"""
Testes de Integração do Serviço Spyne SOAP (soap_service.py).
"""

from unittest.mock import patch
import pytest

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
