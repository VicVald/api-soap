"""
Testes de Integração da API REST e Middlewares FastAPI (test_rest_api.py).
"""

from unittest.mock import MagicMock, patch
import httpx
import pytest
from fastapi.testclient import TestClient

from src.api.rest_routes import SoapRawRequest, processar_soap_raw_envio


class TestRestApiEndpoints:
    """Testes dos endpoints RESTful."""

    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "/soap" in data["soap_endpoint"]
        assert "/soap?wsdl" in data["wsdl_contract"]

    def test_dashboard_root_html(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Portal de Serviços de CEP" in response.text
        assert "SOAP 1.1" in response.text

    def test_openapi_docs_endpoint(self, client: TestClient):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] != ""
        assert "/api/v1/cep/{cep}" in data["paths"]
        assert "/api/v1/status" in data["paths"]

    def test_obter_status_api(self, client: TestClient):
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OPERACIONAL"
        assert "seguranca" in data

    @patch("src.api.rest_routes.consultar_viacep")
    def test_consultar_cep_autorizado(self, mock_consultar, client: TestClient, auth_headers, sample_viacep_response):
        mock_consultar.return_value = sample_viacep_response

        response = client.get("/api/v1/cep/01001000", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["cep"] == "01001-000"
        assert data["logradouro"] == "Praça da Sé"
        assert data["sucesso"] is True

    @patch("src.api.rest_routes.consultar_viacep")
    def test_consultar_cep_bearer_auth(self, mock_consultar, client: TestClient, bearer_headers, sample_viacep_response):
        mock_consultar.return_value = sample_viacep_response

        response = client.get("/api/v1/cep/01001000", headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["cep"] == "01001-000"

    def test_consultar_cep_sem_autenticacao(self, client: TestClient):
        response = client.get("/api/v1/cep/01001000")
        assert response.status_code == 401
        assert "Acesso não autorizado" in response.json()["detail"]

    def test_consultar_cep_autenticacao_invalida(self, client: TestClient):
        response = client.get("/api/v1/cep/01001000", headers={"X-API-Key": "chave-falsa"})
        assert response.status_code == 401

    def test_consultar_cep_formato_invalido(self, client: TestClient, auth_headers):
        response = client.get("/api/v1/cep/123", headers=auth_headers)
        assert response.status_code == 400
        assert "inválido" in response.json()["detail"]

    @patch("src.api.rest_routes.consultar_viacep")
    def test_consultar_cep_nao_encontrado(self, mock_consultar, client: TestClient, auth_headers):
        mock_consultar.return_value = None

        response = client.get("/api/v1/cep/99999999", headers=auth_headers)
        assert response.status_code == 404
        assert "não foi encontrado" in response.json()["detail"]

    def test_validar_cep_endpoint_valido(self, client: TestClient):
        response = client.get("/api/v1/cep/validar/01001000")
        assert response.status_code == 200
        data = response.json()
        assert data["valido"] is True
        assert data["cep_formatado"] == "01001-000"

    def test_validar_cep_endpoint_invalido(self, client: TestClient):
        response = client.get("/api/v1/cep/validar/123")
        assert response.status_code == 200
        data = response.json()
        assert data["valido"] is False

    @patch("src.api.rest_routes.buscar_viacep_por_logradouro")
    def test_buscar_logradouro_autorizado(self, mock_buscar, client: TestClient, auth_headers, sample_viacep_response):
        mock_buscar.return_value = [sample_viacep_response]

        response = client.get(
            "/api/v1/cep/buscar/enderecos?uf=SP&cidade=São Paulo&logradouro=Praça da Sé",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["logradouro"] == "Praça da Sé"

    def test_buscar_logradouro_sem_auth(self, client: TestClient):
        response = client.get("/api/v1/cep/buscar/enderecos?uf=SP&cidade=São Paulo&logradouro=Paulista")
        assert response.status_code == 401

    def test_security_verify_sucesso(self, client: TestClient, auth_headers):
        response = client.get("/api/v1/security/verify", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["autenticado"] is True
        assert data["token_utilizado"] == "soap-secret-key-2026"

    def test_security_verify_falha(self, client: TestClient):
        response = client.get("/api/v1/security/verify")
        assert response.status_code == 401

    def test_executar_soap_raw_function(self):
        mock_client = MagicMock(spec=httpx.Client)
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.text = "<soap:Envelope>ok</soap:Envelope>"
        mock_res.headers = {"content-type": "text/xml"}
        mock_client.post.return_value = mock_res

        req = SoapRawRequest(
            xml_envelope="<xml></xml>",
            soap_action="consultar_cep",
        )
        res = processar_soap_raw_envio(req, client=mock_client)
        assert res.status_code == 200
        assert "<soap:Envelope>ok</soap:Envelope>" in res.response_xml

    def test_executar_soap_raw_function_exception(self):
        mock_client = MagicMock(spec=httpx.Client)
        mock_client.post.side_effect = Exception("Erro interno")

        req = SoapRawRequest(xml_envelope="<xml></xml>")
        res = processar_soap_raw_envio(req, client=mock_client)
        assert res.status_code == 500
        assert "Falha ao processar" in res.response_xml



class TestMiddlewaresSecurity:
    """Testes dos middlewares de segurança HTTP e Rate Limiting."""

    def test_security_headers_injected(self, client: TestClient):
        response = client.get("/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_rate_limit_headers_injected(self, client: TestClient):
        response = client.get("/api/v1/status")
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers

    def test_rate_limiting_exceeded(self, client: TestClient):
        for _ in range(60):
            res = client.get("/api/v1/status")
            assert res.status_code == 200

        response = client.get("/api/v1/status")
        assert response.status_code == 429
        assert "Retry-After" in response.headers
        assert response.json()["error"] == "Too Many Requests"

    def test_executar_soap_raw_endpoint_http(self, client: TestClient):
        with patch("src.api.rest_routes.httpx.Client") as mock_http_cls:
            mock_inst = MagicMock()
            mock_res = MagicMock()
            mock_res.status_code = 200
            mock_res.text = "<soap:Envelope>ok</soap:Envelope>"
            mock_res.headers = {"content-type": "text/xml"}
            mock_inst.__enter__.return_value.post.return_value = mock_res
            mock_http_cls.return_value = mock_inst

            response = client.post(
                "/api/v1/soap/raw",
                json={"xml_envelope": "<xml></xml>", "soap_action": "consultar_cep"},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status_code"] == 200
            assert "<soap:Envelope>ok</soap:Envelope>" in data["response_xml"]

    def test_rate_limiter_with_x_forwarded_for(self, client: TestClient):
        response = client.get("/api/v1/status", headers={"X-Forwarded-For": "203.0.113.195, 70.41.3.18"})
        assert response.status_code == 200
        assert "X-RateLimit-Limit" in response.headers


