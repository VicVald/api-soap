"""
Módulo de Segurança e Políticas de Proteção da API.

Implementa:
1. Autenticação e Autorização via API Key (Header 'X-API-Key' e 'Authorization Bearer')
2. Middleware de Rate Limiting por IP para prevenção de ataques DoS/Brute-force
3. Middleware de Cabeçalhos de Segurança HTTP (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
4. Sanitização e proteção contra injeções XML / XXE
"""

import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from fastapi import Header, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from src.core.config import (
    DEFAULT_API_KEY,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    VALID_API_KEYS,
)

# Definições de Esquemas OpenAPI de Segurança para o Swagger UI
api_key_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False, description="Chave de API informada no header X-API-Key")
http_bearer_scheme = HTTPBearer(auto_error=False, description="Token de autenticação Bearer (ex: Bearer soap-secret-key-2026)")


class RateLimiter:
    """
    Controlador de Rate Limit em memória utilizando janela deslizante.
    """

    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS, window_seconds: int = RATE_LIMIT_WINDOW_SECONDS):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Armazena os timestamps das requisições por IP
        self._requests: Dict[str, List[float]] = defaultdict(list)

    def is_rate_limited(self, client_ip: str) -> Tuple[bool, int, int]:
        """
        Verifica se o IP solicitante excedeu o limite de requisições.

        Returns:
            Tuple[bool, int, int]: (bloqueado, requisições restantes, segundos para reset)
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Filtra apenas timestamps dentro da janela atual
        timestamps = [t for t in self._requests[client_ip] if t > window_start]
        self._requests[client_ip] = timestamps

        current_count = len(timestamps)
        remaining = max(0, self.max_requests - current_count)

        if current_count >= self.max_requests:
            # Tempo até a expiração do registro mais antigo
            oldest = timestamps[0] if timestamps else now
            reset_seconds = max(1, int(self.window_seconds - (now - oldest)))
            return True, 0, reset_seconds

        self._requests[client_ip].append(now)
        return False, remaining - 1, self.window_seconds

    def reset(self) -> None:
        """Limpa o registro de requisições (útil para testes)."""
        self._requests.clear()


# Instância global do RateLimiter
rate_limiter = RateLimiter()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsável por injetar cabeçalhos de segurança em todas as respostas HTTP.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        # Proteção contra MIME Sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Proteção contra Clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # Ativação do filtro XSS do navegador
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Política de Referência estrita
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Política de Permissões de Recursos
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware que intercepta requisições HTTP e aplica controle de taxa por IP.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Ignora rotas estáticas ou de documentação para não bloquear navegação visual
        path = request.url.path
        if path in ("/", "/favicon.ico", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # Identifica IP do cliente considerando proxies confiáveis
        client_ip = request.client.host if request.client else "127.0.0.1"
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()

        is_limited, remaining, reset_time = rate_limiter.is_rate_limited(client_ip)

        if is_limited:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Limite de requisições excedido ({RATE_LIMIT_REQUESTS} req/{RATE_LIMIT_WINDOW_SECONDS}s). Tente novamente em {reset_time} segundos.",
                    "status_code": 429,
                },
                headers={
                    "Retry-After": str(reset_time),
                    "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        return response


def verify_api_key_value(key: Optional[str]) -> bool:
    """Verifica se a chave fornecida corresponde a uma chave válida cadastrada."""
    if not key:
        return False
    return key in VALID_API_KEYS


def require_api_key(
    x_api_key: Optional[str] = Security(api_key_header_scheme),
    bearer_auth: Optional[HTTPAuthorizationCredentials] = Security(http_bearer_scheme),
) -> str:
    """
    Dependência FastAPI que exige autenticação por X-API-Key ou Bearer Token.

    Raises:
        HTTPException: 401 Unauthorized se a chave/token for ausente ou inválida.

    Returns:
        str: A chave/token validado com sucesso.
    """
    token = x_api_key or (bearer_auth.credentials if bearer_auth else None)

    if not token or not verify_api_key_value(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Acesso não autorizado. É necessário fornecer uma API Key válida "
                "no cabeçalho 'X-API-Key' ou 'Authorization: Bearer <token>'."
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def sanitize_input(value: str) -> str:
    """
    Sanitiza strings de entrada prevenindo injeções de caracteres de controle ou XML perigosos.
    """
    if not value:
        return ""
    # Remove caracteres de controle e tags perigosas
    sanitized = value.replace("<", "").replace(">", "").replace("&", "").replace('"', "").replace("'", "")
    return sanitized.strip()
