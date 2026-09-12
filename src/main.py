"""
Aplicação Principal da API Servidor SOAP de CEP.

Este arquivo inicializa o framework FastAPI, monta a aplicação WSGI do Spyne
no caminho `/soap` e disponibiliza a página de documentação e WSDL.
"""

from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from src.services.soap_service import wsgi_soap_app

# Inicialização da aplicação web principal
app = FastAPI(
    title="API Servidor SOAP de CEP",
    description="Servidor SOAP nativo em Python 3.11 com gerador de contrato WSDL e integração dinâmica ao ViaCEP.",
    version="1.0.0",
)

# Monta o servidor WSGI SOAP do Spyne na rota /soap usando a2wsgi (compatível com ASGI)
app.mount("/soap", WSGIMiddleware(wsgi_soap_app))


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    """
    Página inicial com informações da API e links diretos para o contrato WSDL.

    Returns:
        str: Conteúdo HTML estilizado da página inicial.
    """
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Servidor SOAP - Consulta de CEP</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 2rem; margin: 0; }
            .container { max-width: 850px; margin: auto; background-color: #1e293b; border-radius: 12px; padding: 2.5rem; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
            h1 { color: #38bdf8; margin-top: 0; font-size: 2rem; }
            p { font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; }
            .endpoint { background-color: #334155; padding: 12px 18px; border-left: 5px solid #38bdf8; margin: 15px 0; border-radius: 6px; }
            code { background-color: #0f172a; color: #a5f3fc; padding: 3px 8px; border-radius: 4px; font-family: 'Fira Code', monospace; }
            a { color: #38bdf8; text-decoration: none; font-weight: 600; }
            a:hover { text-decoration: underline; }
            ul { line-height: 1.8; color: #e2e8f0; }
            pre { background-color: #0f172a; padding: 15px; border-radius: 8px; overflow-x: auto; color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Servidor API SOAP - Consulta de CEP</h1>
            <p>Serviço no protocolo SOAP 1.1 nativo rodando em <strong>Python 3.11</strong> com contrato WSDL e integração dinâmica ao ViaCEP.</p>

            <h3>📌 Endpoints e Contratos SOAP</h3>
            <div class="endpoint">
                <strong>WSDL Contract URL:</strong> <a href="/soap?wsdl" target="_blank">http://localhost:8000/soap?wsdl</a>
            </div>
            <div class="endpoint">
                <strong>Serviço SOAP (POST URL):</strong> <code>http://localhost:8000/soap</code>
            </div>

            <h3>🛠️ Métodos Disponíveis no Contrato WSDL:</h3>
            <ul>
                <li><code>consultar_cep(cep: string)</code> - Retorna logradouro, bairro, cidade, UF, código IBGE, DDD, etc.</li>
                <li><code>validar_cep(cep: string)</code> - Valida formato de 8 dígitos numéricos e retorna o CEP formatado.</li>
                <li><code>buscar_por_logradouro(uf: string, cidade: string, logradouro: string)</code> - Pesquisa lista de endereços por estado, cidade e rua.</li>
            </ul>

            <h3>💡 Como consumir com Zeep (Cliente Python):</h3>
            <pre><code>from zeep import Client

client = Client('http://localhost:8000/soap?wsdl')
resposta = client.service.consultar_cep('01001000')
print(resposta)</code></pre>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    # Inicia o servidor Uvicorn escutando na porta 8000
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
