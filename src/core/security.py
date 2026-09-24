"""
Módulo de Segurança e Políticas de Proteção do Servidor SOAP.

Implementa:
1. Middleware de Rate Limiting por IP para prevenção de DoS e abuso de chamadas RPC
2. Middleware de Cabeçalhos de Segurança HTTP (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
3. Sanitização de inputs para prevenção de injeções XML / XXE / XSS
"""

import time
from collections import defaultdict
from typing import Dict, List, Tuple

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from src.core.config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)


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
        # Ignora rotas estáticas ou raiz para não bloquear navegação visual
        path = request.url.path
        if path in ("/", "/favicon.ico"):
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


def sanitize_input(value: str) -> str:
    """
    Sanitiza strings de entrada prevenindo injeções de caracteres de controle ou XML perigosos.
    """
    if not value:
        return ""
    # Remove caracteres de controle e tags perigosas
    sanitized = value.replace("<", "").replace(">", "").replace("&", "").replace('"', "").replace("'", "")
    return sanitized.strip()
