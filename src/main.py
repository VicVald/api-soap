"""
Aplicação Principal do Servidor Híbrido SOAP 1.1 & REST de CEP.

Este módulo inicializa o framework FastAPI, configura os esquemas de segurança OpenAPI,
os middlewares de segurança (Rate Limiting, Security Headers e CORS), monta o serviço
SOAP do Spyne na rota `/soap` e disponibiliza a interface Web interativa na raiz `/`.
"""

from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from src.api.rest_routes import router as rest_router
from src.core.config import APP_DESCRIPTION, APP_NAME, APP_VERSION, HOST, PORT
from src.core.security import RateLimitMiddleware, SecurityHeadersMiddleware
from src.services.soap_service import wsgi_soap_app
from src.views.web_ui import render_dashboard_html

# Inicialização da aplicação web principal com especificações OpenAPI 3.0
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Equipe de Arquitetura de APIs",
        "email": "contato@apis-portfolio.local",
    },
    license_info={
        "name": "MIT License",
    },
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

# 2. Inclusão das Rotas REST da API
app.include_router(rest_router)

# 3. Montagem do Servidor WSGI SOAP do Spyne na rota /soap via a2wsgi (ASGI)
app.mount("/soap", WSGIMiddleware(wsgi_soap_app))


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard_root() -> str:
    """
    Página inicial interativa com portal de execução SOAP/REST, documentação e evidências de segurança.
    """
    return render_dashboard_html()


@app.get("/health", tags=["Health Check"], summary="Checagem de Saúde do Servidor")
def health_check():
    """
    Endpoint simples de verificação de liveness e integridade da aplicação.
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "soap_endpoint": "/soap",
        "wsdl_contract": "/soap?wsdl",
        "docs_swagger": "/docs",
    }


if __name__ == "__main__":
    # Inicia o servidor Uvicorn escutando nas configurações definidas
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
