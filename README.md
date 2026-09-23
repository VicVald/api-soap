# 🏛️ Servidor Híbrido SOAP 1.1 & REST de Consulta de CEP

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SOAP](https://img.shields.io/badge/Protocol-SOAP%201.1%20%2F%20WSDL-orange)]()
[![Tests](https://img.shields.io/badge/Tests-77%20Passed%20(99%25%20Coverage)-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

Aplicação servidora desenvolvida em **Python 3.11** para atender aos requisitos da disciplina de Arquitetura e Integração de APIs. A solução implementa um ecossistema completo para consulta e validação de Códigos de Endereçamento Postal (CEP) do Brasil integrado ao provedor **ViaCEP**, disponibilizando tanto o protocolo **SOAP 1.1 com contrato WSDL dinâmico** quanto uma **API REST com documentação interativa OpenAPI / Swagger**.

---

## 📐 Arquitetura da Solução

```mermaid
flowchart TD
    subgraph Clientes["Clientes & Consumidores"]
        C1["Navegador Web (Web UI Dashboard)"]
        C2["Cliente SOAP (Zeep / SoapUI / Postman)"]
        C3["Cliente REST / HTTP (cURL / Swagger UI)"]
    end

    subgraph Servidor["Servidor de Aplicação (FastAPI / Uvicorn)"]
        direction TB
        M1["Middleware de Cabeçalhos de Segurança (CSP, nosniff, DENY)"]
        M2["Middleware de Rate Limiting por IP (60 req/min)"]
        SEC["Módulo de Autenticação (API Key / Bearer Token)"]
        
        UI["Web UI Interativa (Dashboard /)"]
        REST["Rotas RESTful (/api/v1/* com OpenAPI/Swagger)"]
        SOAP["Serviço Spyne SOAP 1.1 (/soap e /soap?wsdl)"]
    end

    subgraph Integracao["Provedor Externo"]
        VIACEP["API Pública ViaCEP (HTTPS)"]
    end

    C1 --> M1
    C2 --> M1
    C3 --> M1
    M1 --> M2
    M2 --> SEC

    SEC --> UI
    SEC --> REST
    SEC --> SOAP

    REST --> VIACEP
    SOAP --> VIACEP
```

---

## 📁 Estrutura de Diretórios do Projeto

```
api-soap/
├── .env.example                  # Modelo de variáveis de ambiente do projeto
├── pyproject.toml                # Metadados, dependências e configurações de testes
├── README.md                     # Documentação principal da aplicação
├── GUIA_EVIDENCIAS_RELATORIO.md  # Guia passo a passo para captura de prints e evidências
├── src/                          # Código-fonte da aplicação
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada FastAPI, middlewares e inicialização Uvicorn
│   ├── core/                     # Módulos centrais de infraestrutura
│   │   ├── __init__.py
│   │   ├── config.py             # Configurações globais e variáveis operacionais
│   │   └── security.py           # Autenticação, Rate Limiting e cabeçalhos de proteção
│   ├── api/                      # Camada REST e documentação OpenAPI
│   │   ├── __init__.py
│   │   └── rest_routes.py        # Endpoints RESTful, esquemas Pydantic e ponte SOAP Raw
│   ├── services/                 # Regras de negócio e integrações
│   │   ├── __init__.py
│   │   ├── soap_service.py       # Definição RPC do Spyne, modelos e gerador WSDL
│   │   └── viacep_client.py      # Cliente HTTP de comunicação com o ViaCEP
│   └── views/                    # Camada de apresentação
│       ├── __init__.py
│       └── web_ui.py             # Interface Web interativa (Dashboard HTML/CSS/JS)
└── tests/                        # Suíte abrangente de testes automatizados
    ├── __init__.py
    ├── conftest.py               # Fixtures e configurações do Pytest
    ├── test_soap_client.py       # Execução direta de testes do cliente SOAP Zeep
    ├── unit/                     # Testes unitários (100% isolados com Mocks)
    │   ├── test_security.py      # Testes de autenticação, rate limiter e sanitização
    │   └── test_viacep_client.py # Testes de validação, formatação e requisições HTTP
    ├── integration/              # Testes de integração
    │   ├── test_rest_api.py      # Testes de rotas REST, códigos HTTP e middlewares
    │   └── test_soap_service.py  # Testes dos métodos RPC do Spyne
    ├── contract/                 # Testes de contrato
    │   └── test_wsdl_contract.py # Validação de schema WSDL, operações e tipos SOAP
    └── e2e/                      # Testes End-to-End
        └── test_soap_client.py   # Testes automatizados com cliente Zeep
```

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- **Linguagem**: Python 3.11 com gerenciador de ambiente e pacotes **`uv`**
- **Framework SOAP**: **Spyne 2.14** (RPC nativo, modelos XML tipados e contrato WSDL 1.1)
- **Framework Web/REST**: **FastAPI 0.115** & **Uvicorn 0.30** (ASGI assíncrono de alta performance)
- **Adaptador WSGI/ASGI**: **`a2wsgi`** para acoplamento do Spyne SOAP dentro do FastAPI
- **Cliente HTTP**: **`httpx`** para consumo da API do ViaCEP
- **Cliente SOAP**: **`zeep`** para testes e consumo automatizado do WSDL
- **Testes & Cobertura**: **`pytest`**, **`pytest-cov`**, **`pytest-mock`** com 99% de cobertura

---

## 🔒 Recursos de Segurança Implementados

1. **Autenticação e Autorização por API Key**:
   - Proteção de endpoints via cabeçalho HTTP `X-API-Key: soap-secret-key-2026` ou `Authorization: Bearer soap-secret-key-2026`.
   - Bloqueio imediato com código `401 Unauthorized` para requisições sem credenciais válidas.
2. **Controle de Taxa de Requisições (Rate Limiting)**:
   - Limitação de taxa de 60 requisições por minuto por endereço IP utilizando janela deslizante.
   - Resposta `429 Too Many Requests` com cabeçalhos `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` e `Retry-After`.
3. **Cabeçalhos de Segurança HTTP (Security Headers)**:
   - `X-Content-Type-Options: nosniff` (prevenção contra MIME Sniffing).
   - `X-Frame-Options: DENY` (mitigação de Clickjacking).
   - `X-XSS-Protection: 1; mode=block` (filtro XSS do navegador).
   - `Referrer-Policy: strict-origin-when-cross-origin`.
4. **Sanitização de Entradas e Proteção XXE**:
   - Parser XML Spyne com validação `lxml` segura.
   - Filtro de caracteres perigosos contra XML Injection e Cross-Site Scripting (XSS).

---

## 🚀 Instalação e Execução

### 1. Pré-requisitos
Certifique-se de ter o Python 3.11 e o gerenciador de pacotes `uv` instalados.

### 2. Sincronizar Dependências
```bash
uv sync
```

### 3. Iniciar o Servidor
```bash
uv run python -m src.main
```

Após a inicialização, os serviços estarão acessíveis nas seguintes URLs:

| Recurso | URL | Descrição |
| :--- | :--- | :--- |
| **Portal Web Interativo** | [http://localhost:8000/](http://localhost:8000/) | Interface gráfica completa para testes |
| **Documentação Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa OpenAPI 3.0 |
| **Documentação ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Especificação visual alternativa OpenAPI |
| **Contrato WSDL (SOAP)** | [http://localhost:8000/soap?wsdl](http://localhost:8000/soap?wsdl) | Definição XML WSDL do serviço SOAP |
| **Endpoint SOAP 1.1 (POST)** | `http://localhost:8000/soap` | Endpoint para envio de envelopes SOAP |
| **Health Check** | [http://localhost:8000/health](http://localhost:8000/health) | Verificação de integridade da aplicação |

---

## 📑 Métodos Disponíveis nos Contratos

### Métodos do Contrato SOAP (WSDL)
- `consultar_cep(cep: string) -> EnderecoResponse`: Consulta dados detalhados do CEP (Logradouro, Bairro, Cidade, UF, IBGE, DDD, SIAFI).
- `validar_cep(cep: string) -> ResultadoValidacao`: Valida o formato numérico de 8 dígitos e devolve a máscara `00000-000`.
- `buscar_por_logradouro(uf: string, cidade: string, logradouro: string) -> Array(EnderecoResponse)`: Pesquisa endereços por estado, cidade e rua.
- `obter_status_servico() -> StatusServicoResponse`: Retorna integridade e status operacional do serviço SOAP.

### Endpoints da API REST (OpenAPI / Swagger)
- `GET /api/v1/cep/{cep}`: Consulta endereço por CEP (requer API Key).
- `GET /api/v1/cep/validar/{cep}`: Valida formato de CEP.
- `GET /api/v1/cep/buscar/enderecos?uf=SP&cidade=São Paulo&logradouro=Sé`: Busca por logradouro (requer API Key).
- `GET /api/v1/security/verify`: Demonstração de validação de autenticação (requer API Key).
- `GET /api/v1/status`: Informações de status e recursos de segurança ativos.
- `POST /api/v1/soap/raw`: Executor / ponte REST para envio de envelopes SOAP XML.

---

## 🧪 Executando a Suíte de Testes Automatizados

Para rodar todos os 77 testes automatizados com relatório de cobertura em terminal e geração de HTML:

```bash
uv run pytest
```

Para abrir o relatório visual de cobertura em HTML gerado em `coverage_html/index.html`:
```bash
# No Linux:
xdg-open coverage_html/index.html
```

Para executar o cliente de teste SOAP Zeep de ponta a ponta com o servidor ativo:
```bash
uv run python -m tests.test_soap_client
```

---

## 📬 Exemplos Práticos de Requisição

### 1. Requisição SOAP Raw (cURL)
```bash
curl -X POST http://localhost:8000/soap \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: consultar_cep" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:consultar_cep>
         <spy:cep>01001000</spy:cep>
      </spy:consultar_cep>
   </soapenv:Body>
</soapenv:Envelope>'
```

### 2. Requisição REST com Autenticação (cURL)
```bash
curl -X GET "http://localhost:8000/api/v1/cep/01001000" \
  -H "X-API-Key: soap-secret-key-2026"
```

### 3. Requisição REST Sem Autenticação (Retorno 401 Unauthorized para Evidência)
```bash
curl -i -X GET "http://localhost:8000/api/v1/cep/01001000"
```

---

## 📸 Guia para o Relatório Acadêmico

Consulte o arquivo **[`GUIA_EVIDENCIAS_RELATORIO.md`](file:///home/victor/Documents/agents-portfolio/api-soap/GUIA_EVIDENCIAS_RELATORIO.md)** para o roteiro completo de capturas de tela exigidas no trabalho (Telas em Funcionamento, Segurança, Swagger/WSDL e Testes de Cobertura).
