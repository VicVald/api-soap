"""
Testes de Contrato da Interface WSDL e Protocolo SOAP 1.1 (test_wsdl_contract.py).
"""

from unittest.mock import patch
from xml.etree import ElementTree as ET
import pytest
from fastapi.testclient import TestClient


class TestWsdlContract:
    """Testes de validação do contrato WSDL e conformidade SOAP 1.1."""

    def test_wsdl_endpoint_returns_xml(self, client: TestClient):
        response = client.get("/soap?wsdl")
        assert response.status_code == 200
        assert "text/xml" in response.headers.get("content-type", "")

        # Parse do XML WSDL
        root = ET.fromstring(response.text)
        # O nome da tag raiz deve terminar com definitions
        assert "definitions" in root.tag.lower()
        # Valida namespace de destino (tns)
        assert root.attrib.get("targetNamespace") == "api.soap.cep"

    def test_wsdl_declares_all_operations(self, client: TestClient):
        response = client.get("/soap?wsdl")
        wsdl_content = response.text

        # Valida se todas as 4 operações RPC estão formalmente declaradas no WSDL
        assert "consultar_cep" in wsdl_content
        assert "validar_cep" in wsdl_content
        assert "buscar_por_logradouro" in wsdl_content
        assert "obter_status_servico" in wsdl_content

    def test_wsdl_declares_complex_types(self, client: TestClient):
        response = client.get("/soap?wsdl")
        wsdl_content = response.text

        # Valida se os modelos de dados (ComplexTypes) estão no schema XML
        assert "EnderecoResponse" in wsdl_content
        assert "ResultadoValidacao" in wsdl_content
        assert "StatusServicoResponse" in wsdl_content

    def test_soap_post_envelope_validar_cep(self, client: TestClient):
        envelope = (
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">\n'
            "   <soapenv:Header/>\n"
            "   <soapenv:Body>\n"
            "      <spy:validar_cep>\n"
            "         <spy:cep>01001-000</spy:cep>\n"
            "      </spy:validar_cep>\n"
            "   </soapenv:Body>\n"
            "</soapenv:Envelope>"
        )
        response = client.post(
            "/soap",
            content=envelope,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "validar_cep",
            },
        )
        assert response.status_code == 200
        assert "validar_cepResponse" in response.text
        assert "valido>true" in response.text
        assert "01001-000" in response.text

    @patch("src.services.soap_service.consultar_viacep")
    def test_soap_post_envelope_consultar_cep(self, mock_consultar, client: TestClient, sample_viacep_response):
        mock_consultar.return_value = sample_viacep_response
        envelope = (
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">\n'
            "   <soapenv:Header/>\n"
            "   <soapenv:Body>\n"
            "      <spy:consultar_cep>\n"
            "         <spy:cep>01001-000</spy:cep>\n"
            "      </spy:consultar_cep>\n"
            "   </soapenv:Body>\n"
            "</soapenv:Envelope>"
        )
        response = client.post(
            "/soap",
            content=envelope,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "consultar_cep",
            },
        )
        assert response.status_code == 200
        assert "consultar_cepResponse" in response.text
        assert "Praça da Sé" in response.text
        assert "sucesso>true" in response.text

    @patch("src.services.soap_service.buscar_viacep_por_logradouro")
    def test_soap_post_envelope_buscar_logradouro(self, mock_buscar, client: TestClient, sample_viacep_response):
        mock_buscar.return_value = [sample_viacep_response]
        envelope = (
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">\n'
            "   <soapenv:Header/>\n"
            "   <soapenv:Body>\n"
            "      <spy:buscar_por_logradouro>\n"
            "         <spy:uf>SP</spy:uf>\n"
            "         <spy:cidade>São Paulo</spy:cidade>\n"
            "         <spy:logradouro>Praça da Sé</spy:logradouro>\n"
            "      </spy:buscar_por_logradouro>\n"
            "   </soapenv:Body>\n"
            "</soapenv:Envelope>"
        )
        response = client.post(
            "/soap",
            content=envelope,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "buscar_por_logradouro",
            },
        )
        assert response.status_code == 200
        assert "buscar_por_logradouroResponse" in response.text
        assert "Praça da Sé" in response.text

    def test_soap_post_envelope_obter_status(self, client: TestClient):
        envelope = (
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">\n'
            "   <soapenv:Header/>\n"
            "   <soapenv:Body>\n"
            "      <spy:obter_status_servico/>\n"
            "   </soapenv:Body>\n"
            "</soapenv:Envelope>"
        )
        response = client.post(
            "/soap",
            content=envelope,
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "obter_status_servico",
            },
        )
        assert response.status_code == 200
        assert "obter_status_servicoResponse" in response.text
        assert "OPERACIONAL" in response.text
