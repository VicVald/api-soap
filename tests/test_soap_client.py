"""
Script e Testes do Cliente SOAP.

Este módulo utiliza a biblioteca `zeep` para conectar ao WSDL do servidor SOAP
e testar a execução de todos os métodos RPC disponíveis.
"""

import sys
from zeep import Client

# URL do contrato WSDL gerado pelo servidor SOAP Spyne
WSDL_URL: str = "http://localhost:8000/soap?wsdl"


def testar_servico_soap() -> None:
    """
    Conecta ao serviço SOAP via WSDL e executa casos de teste para:
    1. Validação de formato de CEP (`validar_cep`)
    2. Consulta de CEP válido (`consultar_cep`)
    3. Consulta de CEP inexistente (`consultar_cep`)
    4. Busca por logradouro (`buscar_por_logradouro`)
    """
    print("=" * 65)
    print("🚀 TESTANDO CLIENTE SOAP (ZEEP) - API CEP (PYTHON 3.11 NATIVO)")
    print("=" * 65)

    try:
        print(f"Conectando ao contrato WSDL: {WSDL_URL} ...")
        # Instancia o cliente Zeep parseando a especificação WSDL do servidor
        client = Client(WSDL_URL)
        print("✅ Conexão com o contrato WSDL realizada com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao conectar no WSDL ({WSDL_URL}): {e}")
        print("Certifique-se de que o servidor SOAP está ativo (`uv run python -m src.main`).")
        sys.exit(1)

    # ------------------------------------------------------------
    # Caso 1: Testar o método validar_cep
    # ------------------------------------------------------------
    print("------------------------------------------------------------")
    print("1️⃣ Testando método: validar_cep('01001-000')")
    res_val = client.service.validar_cep("01001-000")
    print(f"   Válido: {res_val.valido}")
    print(f"   Mensagem: {res_val.mensagem}")
    print(f"   CEP Formatado: {res_val.cep_formatado}")
    assert res_val.valido is True

    # ------------------------------------------------------------
    # Caso 2: Testar a consulta de um CEP Válido
    # ------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("2️⃣ Testando método: consultar_cep('01001000') (Praça da Sé - SP)")
    res_cep = client.service.consultar_cep("01001000")
    print(f"   Sucesso: {res_cep.sucesso}")
    print(f"   Logradouro: {res_cep.logradouro}")
    print(f"   Bairro: {res_cep.bairro}")
    print(f"   Cidade/UF: {res_cep.localidade} - {res_cep.uf}")
    print(f"   CEP: {res_cep.cep}")
    print(f"   IBGE: {res_cep.ibge}")
    print(f"   DDD: {res_cep.ddd}")
    assert res_cep.sucesso is True
    assert res_cep.uf == "SP"

    # ------------------------------------------------------------
    # Caso 3: Testar a consulta de um CEP Inexistente
    # ------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("3️⃣ Testando método: consultar_cep('99999999') (Inexistente)")
    res_invalido = client.service.consultar_cep("99999999")
    print(f"   Sucesso: {res_invalido.sucesso}")
    print(f"   Mensagem: {res_invalido.mensagem}")
    assert res_invalido.sucesso is False

    # ------------------------------------------------------------
    # Caso 4: Testar a busca por Logradouro / Rua
    # ------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("4️⃣ Testando método: buscar_por_logradouro('RS', 'Porto Alegre', 'Domingos')")
    res_busca = client.service.buscar_por_logradouro("RS", "Porto Alegre", "Domingos")
    print(f"   Quantidade de resultados encontrados: {len(res_busca)}")
    for idx, item in enumerate(res_busca[:3], 1):
        print(f"   - Endereço #{idx}: {item.logradouro} | Bairro: {item.bairro} | CEP: {item.cep}")
    assert len(res_busca) > 0

    print("\n" + "=" * 65)
    print("✨ TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO EM PYTHON 3.11!")
    print("=" * 65)


if __name__ == "__main__":
    testar_servico_soap()
