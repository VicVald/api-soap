"""
Testes de Integração do Serviço Spyne SOAP e Servidor Web.
"""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from src.core.config import RATE_LIMIT_REQUESTS
from src.core.security import rate_limiter
from src.services.soap_service import (
    CepService,
    EnderecoResponse,
    ResultadoValidacao,
    StatusServicoResponse,
)


class TestCepServiceDirectCalls:
    """Testes de execução direta dos métodos RPC da classe CepService."""

    @patch("src.services.soap_service.consultar_viacep")
    def test_consultar_cep_sucesso(self, mock_consultar, sample_viacep_response):
        mock_consultar.return_value = sample_viacep_response

        resposta: EnderecoResponse = CepService.consultar_cep(None, "01001000")
        assert resposta.sucesso is True
        assert resposta.cep == "01001-000"
        assert resposta.logradouro == "Praça da Sé"
        assert resposta.uf == "SP"
        assert resposta.mensagem == "CEP encontrado com sucesso."

    @patch("src.services.soap_service.consultar_viacep")
    def test_consultar_cep_inexistente(self, mock_consultar):
        mock_consultar.return_value = None

        resposta: EnderecoResponse = CepService.consultar_cep(None, "99999999")
        assert resposta.sucesso is False
        assert "não foi localizado" in resposta.mensagem

    def test_consultar_cep_vazio(self):
        resposta: EnderecoResponse = CepService.consultar_cep(None, "")
        assert resposta.sucesso is False
        assert "obrigatório" in resposta.mensagem

    def test_validar_cep_valido(self):
        resposta: ResultadoValidacao = CepService.validar_cep(None, "01001000")
        assert resposta.valido is True
        assert resposta.cep_formatado == "01001-000"

    def test_validar_cep_invalido(self):
        resposta: ResultadoValidacao = CepService.validar_cep(None, "123")
        assert resposta.valido is False
        assert "inválido" in resposta.mensagem

    def test_validar_cep_vazio(self):
        resposta: ResultadoValidacao = CepService.validar_cep(None, "")
        assert resposta.valido is False
        assert "não foi informado" in resposta.mensagem

    @patch("src.services.soap_service.buscar_viacep_por_logradouro")
    def test_buscar_por_logradouro_sucesso(self, mock_buscar, sample_viacep_response):
        mock_buscar.return_value = [sample_viacep_response]

        resultados = CepService.buscar_por_logradouro(None, "SP", "São Paulo", "Praça da Sé")
        assert len(resultados) == 1
        assert resultados[0].logradouro == "Praça da Sé"
        assert resultados[0].sucesso is True

    def test_buscar_por_logradouro_parametros_vazios(self):
        resultados = CepService.buscar_por_logradouro(None, "", "", "")
        assert resultados == []

    def test_obter_status_servico(self):
        status_res: StatusServicoResponse = CepService.obter_status_servico(None)
        assert status_res.status == "OPERACIONAL"
        assert status_res.provedor == "ViaCEP Integration Engine"
        assert status_res.versao != ""


class TestWebUiAndEndpoints:
    """Testes dos endpoints HTTP da aplicação (Interface Gráfica e Health Check)."""

    def test_dashboard_root_html(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "SOAP 1.1 CEP Service" in response.text
        assert "consultar_cep" in response.text
        assert "validar_cep" in response.text
        assert "buscar_por_logradouro" in response.text

    def test_health_check_endpoint(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        dados = response.json()
        assert dados["status"] == "healthy"
        assert dados["soap_endpoint"] == "/soap"
        assert dados["wsdl_contract"] == "/soap?wsdl"
        assert "SOAP 1.1" in dados["protocol"]


class TestMiddlewaresSecurity:
    """Testes dos Middlewares de Segurança aplicados ao servidor SOAP."""

    def test_security_headers_injected(self, client: TestClient):
        response = client.get("/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert "mode=block" in response.headers.get("X-XSS-Protection", "")
        assert "strict-origin-when-cross-origin" in response.headers.get("Referrer-Policy", "")

    def test_rate_limit_headers_injected(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers

    def test_rate_limiting_exceeded(self, client: TestClient):
        for _ in range(RATE_LIMIT_REQUESTS):
            res = client.get("/health", headers={"X-Forwarded-For": "198.51.100.99"})
            assert res.status_code == 200

        # Requisição acima do limite deve retornar HTTP 429
        res_bloqueada = client.get("/health", headers={"X-Forwarded-For": "198.51.100.99"})
        assert res_bloqueada.status_code == 429
        assert "Too Many Requests" in res_bloqueada.text
        assert "Retry-After" in res_bloqueada.headers

    def test_rate_limiter_with_x_forwarded_for(self, client: TestClient):
        res1 = client.get("/health", headers={"X-Forwarded-For": "203.0.113.1, 10.0.0.1"})
        assert res1.status_code == 200
        assert int(res1.headers.get("X-RateLimit-Remaining", 0)) == RATE_LIMIT_REQUESTS - 1
