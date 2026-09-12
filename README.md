# API SOAP de Consulta de CEP em Python

Uma API Servidor no protocolo **SOAP 1.1** desenvolvida em Python 3.11 com **Spyne**, **FastAPI** e **Uvicorn**. O servidor expõe contratos WSDL dinâmicos e integra-se em tempo real com a API REST do ViaCEP.

---

## 📁 Estrutura de Arquivos do Projeto

```
api-soap/
├── src/                        # Código-fonte da aplicação
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada FastAPI/Uvicorn
│   └── services/               # Módulos de serviços
│       ├── __init__.py
│       ├── soap_service.py     # Definição do Serviço Spyne SOAP e modelos XML
│       └── viacep_client.py    # Cliente HTTP de integração com ViaCEP
├── tests/                      # Suite de testes
│   ├── __init__.py
│   └── test_soap_client.py     # Testes automatizados SOAP com Zeep
├── pyproject.toml              # Dependências e metadados do projeto
├── README.md                   # Documentação do projeto
└── .python-version             # Configuração da versão do Python (3.11)
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** com gerenciador de pacotes **`uv`**
- **Spyne**: Definição de RPC, modelos de dados XML e gerador de WSDL
- **FastAPI / Uvicorn**: Servidor Web assíncrono para montagem do WSGI SOAP via `a2wsgi`
- **httpx**: Cliente HTTP para consultar a API do ViaCEP
- **Zeep**: Cliente Python SOAP utilizado nos testes

---

## 🚀 Como Executar o Projeto

### 1. Instalar as Dependências

Certifique-se de ter o `uv` instalado e execute:

```bash
uv sync
```

### 2. Iniciar o Servidor SOAP

Para iniciar o servidor HTTP/SOAP na porta `8000`:

```bash
uv run python -m src.main
```

O servidor estará disponível em:
- **Página Inicial**: [http://localhost:8000/](http://localhost:8000/)
- **Serviço SOAP Endpoint (POST)**: `http://localhost:8000/soap`
- **WSDL (GET)**: [http://localhost:8000/soap?wsdl](http://localhost:8000/soap?wsdl)

---

## 🧪 Como Executar os Testes

Com o servidor rodando em um terminal, abra outro terminal e execute os testes do cliente SOAP:

```bash
uv run python -m tests.test_soap_client
```

O script testará automaticamente as chamadas RPC SOAP no WSDL:
1. `validar_cep`
2. `consultar_cep` (CEP Válido)
3. `consultar_cep` (CEP Inexistente)
4. `buscar_por_logradouro`

---

## 📬 Exemplo de Requisição SOAP Raw (XML / cURL)

Você pode enviar requisições diretas via `curl` ou Postman utilizando o formato Envelope XML SOAP:

### Consulta de CEP:
```bash
curl -X POST http://localhost:8000/soap/ \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: consultar_cep" \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
        <soapenv:Header/>
        <soapenv:Body>
           <spy:consultar_cep>
              <spy:cep>01001000</spy:cep>
           </spy:consultar_cep>
        </soapenv:Body>
     </soapenv:Envelope>'
```
