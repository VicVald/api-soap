"""
Configurações Globais da Aplicação API SOAP & REST.

Centraliza variáveis de ambiente e parâmetros operacionais de segurança,
servidor e integrações externas.
"""

import os
from typing import Set

# Configurações do Servidor
APP_NAME: str = "API de Serviços SOAP & REST - Consulta de CEP"
APP_VERSION: str = "2.0.0"
APP_DESCRIPTION: str = (
    "Servidor híbrido Python 3.11 com serviço nativo SOAP 1.1 (WSDL) e API REST "
    "integrados ao ViaCEP, incluindo recursos avançados de segurança, autenticação "
    "por API Key, rate limiting, documentação OpenAPI/Swagger e suíte completa de testes."
)

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Configurações de Segurança
# Chaves de API autorizadas (exemplo padrão para ambiente de desenvolvimento/avaliação)
DEFAULT_API_KEY: str = os.getenv("API_KEY", "soap-secret-key-2026")
VALID_API_KEYS: Set[str] = {
    DEFAULT_API_KEY,
    "admin-token-academico",
    "cliente-soap-token-123",
}

# Rate Limiting: máximo de requisições por janela de tempo (em segundos)
RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

# URL Base para comunicação com a API ViaCEP
VIACEP_BASE_URL: str = os.getenv("VIACEP_BASE_URL", "https://viacep.com.br/ws")
HTTP_TIMEOUT_SECONDS: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10.0"))
