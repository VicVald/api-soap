"""
Configurações Globais da Aplicação API SOAP.

Centraliza variáveis de ambiente e parâmetros operacionais de segurança,
servidor e integrações externas para o Serviço SOAP de CEP.
"""

import os
from typing import Set

# Configurações do Servidor
APP_NAME: str = "Serviço SOAP 1.1 - Consulta de CEP"
APP_VERSION: str = "2.0.0"
APP_DESCRIPTION: str = (
    "Servidor nativo SOAP 1.1 (WSDL RPC/encoded) em Python 3.11 com Spyne integrado ao ViaCEP, "
    "incluindo interface gráfica mínima de demonstração, rate limiting, security headers e suíte de testes."
)

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Configurações de Segurança
# Rate Limiting: máximo de requisições por janela de tempo (em segundos)
RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

# URL Base para comunicação com a API ViaCEP
VIACEP_BASE_URL: str = os.getenv("VIACEP_BASE_URL", "https://viacep.com.br/ws")
HTTP_TIMEOUT_SECONDS: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10.0"))
