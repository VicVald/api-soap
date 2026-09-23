"""
Testes E2E do Cliente SOAP Zeep.

Pode ser executado diretamente (`uv run python -m tests.e2e.test_soap_client`)
com o servidor rodando, ou via pytest.
"""

import sys
import pytest
from zeep import Client
from zeep.transports import Transport
import httpx

WSDL_URL: str = "http://localhost:8000/soap?wsdl"


def executar_testes_zeep(wsdl_url: str = WSDL_URL) -> bool:
    """
    Executa testes de ponta a ponta com o cliente Zeep consumindo o contrato WSDL.
    """
    print("=" * 65)
    print("🚀 EXECUTANDO TESTES E2E DO CLIENTE SOAP (ZEEP)")
    print("=" * 65)

    try:
        client = Client(wsdl_url)
        print("✅ Contrato WSDL carregado com sucesso!\n")
    except Exception as e:
        print(f"⚠️ Servidor não disponível em {wsdl_url}: {e}")
        return False

    # 1. Teste de Validação de CEP
    print("1️⃣ Testando validar_cep('01001-000')...")
    res_val = client.service.validar_cep("01001-000")
    assert res_val.valido is True
    print(f"   Resultado: Válido={res_val.valido}, Formatado={res_val.cep_formatado}")

    # 2. Teste de Consulta de CEP Válido
    print("\n2️⃣ Testando consultar_cep('01001000')...")
    res_cep = client.service.consultar_cep("01001000")
    assert res_cep.sucesso is True
    assert res_cep.uf == "SP"
    print(f"   Resultado: {res_cep.logradouro} - {res_cep.localidade}/{res_cep.uf}")

    # 3. Teste de Consulta de CEP Inexistente
    print("\n3️⃣ Testando consultar_cep('99999999')...")
    res_invalido = client.service.consultar_cep("99999999")
    assert res_invalido.sucesso is False
    print(f"   Resultado: Sucesso={res_invalido.sucesso}, Mensagem='{res_invalido.mensagem}'")

    # 4. Teste de Busca por Logradouro
    print("\n4️⃣ Testando buscar_por_logradouro('RS', 'Porto Alegre', 'Domingos')...")
    res_busca = client.service.buscar_por_logradouro("RS", "Porto Alegre", "Domingos")
    assert len(res_busca) > 0
    print(f"   Resultado: {len(res_busca)} endereços encontrados.")

    # 5. Teste de Obtenção de Status do Serviço
    print("\n5️⃣ Testando obter_status_servico()...")
    res_status = client.service.obter_status_servico()
    assert res_status.status == "OPERACIONAL"
    print(f"   Resultado: Status={res_status.status}, Provedor={res_status.provedor}")

    print("\n" + "=" * 65)
    print("✨ TODOS OS TESTES E2E DO CLIENTE SOAP PASSARAM COM SUCESSO!")
    print("=" * 65)
    return True


def test_e2e_zeep_integration():
    """
    Teste pytest que verifica a conectividade caso o servidor esteja ativo,
    ou pula o teste caso o servidor local esteja offline.
    """
    try:
        with httpx.Client(timeout=2.0) as http_client:
            res = http_client.get(WSDL_URL)
            if res.status_code != 200:
                pytest.skip("Servidor SOAP local offline para teste E2E Zeep.")
    except Exception:
        pytest.skip("Servidor SOAP local offline para teste E2E Zeep.")

    assert executar_testes_zeep(WSDL_URL) is True


if __name__ == "__main__":
    sucesso = executar_testes_zeep(WSDL_URL)
    if not sucesso:
        sys.exit(1)
