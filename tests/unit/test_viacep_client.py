"""
Testes Unitários do Módulo de Integração ViaCEP (viacep_client.py).
"""

from unittest.mock import MagicMock, patch
import httpx
import pytest

from src.services.viacep_client import (
    buscar_viacep_por_logradouro,
    consultar_viacep,
    formatar_cep,
    limpar_cep,
    validar_formato_cep,
)


class TestLimparCep:
    """Testes para a função limpar_cep."""

    def test_limpar_cep_com_hifen(self):
        assert limpar_cep("01001-000") == "01001000"

    def test_limpar_cep_com_pontos_e_hifen(self):
        assert limpar_cep("01.001-000") == "01001000"

    def test_limpar_cep_com_espacos(self):
        assert limpar_cep("  01001000  ") == "01001000"

    def test_limpar_cep_com_letras(self):
        assert limpar_cep("01A001B000") == "01001000"

    def test_limpar_cep_vazio_ou_none(self):
        assert limpar_cep("") == ""
        assert limpar_cep(None) == ""


class TestValidarFormatoCep:
    """Testes para a função validar_formato_cep."""

    def test_cep_valido_8_digitos(self):
        assert validar_formato_cep("01001000") is True
        assert validar_formato_cep("01001-000") is True

    def test_cep_invalido_menos_de_8_digitos(self):
        assert validar_formato_cep("1234567") is False
        assert validar_formato_cep("123") is False

    def test_cep_invalido_mais_de_8_digitos(self):
        assert validar_formato_cep("123456789") is False

    def test_cep_invalido_vazio(self):
        assert validar_formato_cep("") is False
        assert validar_formato_cep("   ") is False


class TestFormatarCep:
    """Testes para a função formatar_cep."""

    def test_formatar_cep_sem_mascara(self):
        assert formatar_cep("01001000") == "01001-000"

    def test_formatar_cep_ja_formatado(self):
        assert formatar_cep("01001-000") == "01001-000"

    def test_formatar_cep_invalido_retorna_original(self):
        assert formatar_cep("123") == "123"


class TestConsultarViacep:
    """Testes para a função consultar_viacep."""

    def test_consultar_viacep_sucesso(self, sample_viacep_response):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_viacep_response

        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.return_value = mock_response

        resultado = consultar_viacep("01001-000", client=mock_client)
        assert resultado is not None
        assert resultado["cep"] == "01001-000"
        assert resultado["logradouro"] == "Praça da Sé"
        assert resultado["uf"] == "SP"

    def test_consultar_viacep_status_nao_200(self):
        mock_response = MagicMock()
        mock_response.status_code = 500

        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.return_value = mock_response

        resultado = consultar_viacep("01001000", client=mock_client)
        assert resultado is None

    def test_consultar_viacep_cep_inexistente(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"erro": "true"}

        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.return_value = mock_response

        resultado = consultar_viacep("99999999", client=mock_client)
        assert resultado is None

    def test_consultar_viacep_formato_invalido(self):
        resultado = consultar_viacep("123")
        assert resultado is None

    def test_consultar_viacep_erro_conexao(self):
        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.side_effect = httpx.ConnectError("Falha de conexão")

        resultado = consultar_viacep("01001000", client=mock_client)
        assert resultado is None

    @patch("httpx.Client")
    def test_consultar_viacep_cliente_padrao(self, mock_client_cls, sample_viacep_response):
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_viacep_response
        mock_instance.__enter__.return_value.get.return_value = mock_response
        mock_client_cls.return_value = mock_instance

        resultado = consultar_viacep("01001000")
        assert resultado is not None
        assert resultado["localidade"] == "São Paulo"

    @patch("httpx.Client")
    def test_consultar_viacep_cliente_padrao_inexistente(self, mock_client_cls):
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"erro": True}
        mock_instance.__enter__.return_value.get.return_value = mock_response
        mock_client_cls.return_value = mock_instance

        resultado = consultar_viacep("99999999")
        assert resultado is None


class TestBuscarViacepPorLogradouro:
    """Testes para a função buscar_viacep_por_logradouro."""

    def test_buscar_logradouro_sucesso(self, sample_viacep_response):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [sample_viacep_response]

        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.return_value = mock_response

        resultado = buscar_viacep_por_logradouro("SP", "São Paulo", "Praça da Sé", client=mock_client)
        assert isinstance(resultado, list)
        assert len(resultado) == 1
        assert resultado[0]["logradouro"] == "Praça da Sé"

    def test_buscar_logradouro_status_nao_200(self):
        mock_response = MagicMock()
        mock_response.status_code = 500

        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.return_value = mock_response

        resultado = buscar_viacep_por_logradouro("SP", "São Paulo", "Paulista", client=mock_client)
        assert resultado == []

    def test_buscar_logradouro_parametros_invalidos(self):
        # UF com tamanho inválido
        assert buscar_viacep_por_logradouro("S", "São Paulo", "Paulista") == []
        # Logradouro com menos de 3 caracteres
        assert buscar_viacep_por_logradouro("SP", "São Paulo", "Pa") == []
        # Cidade com menos de 3 caracteres
        assert buscar_viacep_por_logradouro("SP", "Sa", "Paulista") == []
        # Parâmetro vazio
        assert buscar_viacep_por_logradouro("", "", "") == []

    def test_buscar_logradouro_erro_conexao(self):
        mock_client = MagicMock(spec=httpx.Client)
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")

        resultado = buscar_viacep_por_logradouro("SP", "São Paulo", "Paulista", client=mock_client)
        assert resultado == []

    @patch("httpx.Client")
    def test_buscar_logradouro_cliente_padrao(self, mock_client_cls, sample_viacep_response):
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [sample_viacep_response]
        mock_instance.__enter__.return_value.get.return_value = mock_response
        mock_client_cls.return_value = mock_instance

        resultado = buscar_viacep_por_logradouro("SP", "São Paulo", "Praça da Sé")
        assert len(resultado) == 1
        assert resultado[0]["logradouro"] == "Praça da Sé"
