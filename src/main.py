"""
Aplicação Principal do Servidor SOAP 1.1 de Consulta de CEP.

Este módulo inicializa a aplicação FastAPI, configura os middlewares de segurança
(Rate Limiting, Security Headers e CORS), monta o serviço SOAP do Spyne na rota `/soap`
via a2wsgi e disponibiliza uma interface gráfica mínima de demonstração na raiz `/`.
"""

from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from src.core.config import APP_DESCRIPTION, APP_NAME, APP_VERSION, HOST, PORT
from src.core.security import RateLimitMiddleware, SecurityHeadersMiddleware
from src.services.soap_service import wsgi_soap_app
from src.views.web_ui import render_dashboard_html

# Inicialização da aplicação web
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# 1. Configuração de Middlewares de Segurança
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# Configuração de CORS para permitir requisições cross-origin controladas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset", "Retry-After"],
)

# 2. Montagem do Servidor WSGI SOAP do Spyne na rota /soap via a2wsgi (ASGI)
app.mount("/soap", WSGIMiddleware(wsgi_soap_app))


@app.get("/", response_class=HTMLResponse)
def dashboard_root() -> str:
    """
    Página inicial com interface gráfica mínima de demonstração do serviço SOAP 1.1.
    """
    return render_dashboard_html()


@app.get("/health", tags=["Health Check"], summary="Checagem de Integridade do Servidor SOAP")
def health_check():
    """
    Endpoint de verificação de liveness e integridade do serviço SOAP.
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "protocol": "SOAP 1.1 (RPC/Encoded)",
        "soap_endpoint": "/soap",
        "wsdl_contract": "/soap?wsdl",
    }


if __name__ == "__main__":
    # Inicia o servidor Uvicorn escutando nas configurações definidas
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
