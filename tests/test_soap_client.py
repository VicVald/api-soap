"""
Módulo de Testes do Cliente SOAP Zeep (Compatibilidade e Execução Direta).
"""

from tests.e2e.test_soap_client import WSDL_URL, executar_testes_zeep

if __name__ == "__main__":
    executar_testes_zeep(WSDL_URL)
