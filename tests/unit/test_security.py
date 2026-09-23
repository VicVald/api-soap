"""
Testes Unitários do Módulo de Segurança (security.py).
"""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.core.security import (
    RateLimiter,
    require_api_key,
    sanitize_input,
    verify_api_key_value,
)


class TestSanitizeInput:
    """Testes da sanitização de entradas contra XML Injection / XSS."""

    def test_sanitize_clean_string(self):
        assert sanitize_input("01001000") == "01001000"

    def test_sanitize_xml_tags(self):
        assert sanitize_input("<script>alert('xss')</script>") == "scriptalert(xss)/script"

    def test_sanitize_quotes_and_ampersand(self):
        assert sanitize_input('foo"bar&baz\'qux') == "foobarbazqux"

    def test_sanitize_empty(self):
        assert sanitize_input("") == ""


class TestVerifyApiKey:
    """Testes para a função verify_api_key_value."""

    def test_valid_default_key(self):
        assert verify_api_key_value("soap-secret-key-2026") is True

    def test_valid_secondary_key(self):
        assert verify_api_key_value("admin-token-academico") is True

    def test_invalid_key(self):
        assert verify_api_key_value("chave-falsa-123") is False

    def test_empty_or_none_key(self):
        assert verify_api_key_value("") is False
        assert verify_api_key_value(None) is False


class TestRequireApiKeyDependency:
    """Testes da dependência FastAPI require_api_key."""

    def test_require_api_key_header_success(self):
        key = require_api_key(x_api_key="soap-secret-key-2026", bearer_auth=None)
        assert key == "soap-secret-key-2026"

    def test_require_api_key_bearer_success(self):
        auth_cred = HTTPAuthorizationCredentials(scheme="Bearer", credentials="soap-secret-key-2026")
        key = require_api_key(x_api_key=None, bearer_auth=auth_cred)
        assert key == "soap-secret-key-2026"

    def test_require_api_key_missing_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(x_api_key=None, bearer_auth=None)
        assert exc_info.value.status_code == 401
        assert "Acesso não autorizado" in exc_info.value.detail

    def test_require_api_key_invalid_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(x_api_key="chave-errada", bearer_auth=None)
        assert exc_info.value.status_code == 401


class TestRateLimiter:
    """Testes unitários da lógica de Rate Limiting."""

    def test_rate_limiter_allows_under_limit(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        for _ in range(5):
            is_limited, remaining, _ = limiter.is_rate_limited("192.168.1.1")
            assert is_limited is False

    def test_rate_limiter_blocks_over_limit(self):
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        limiter.is_rate_limited("192.168.1.2")
        limiter.is_rate_limited("192.168.1.2")
        limiter.is_rate_limited("192.168.1.2")

        is_limited, remaining, reset_time = limiter.is_rate_limited("192.168.1.2")
        assert is_limited is True
        assert remaining == 0
        assert reset_time > 0

    def test_rate_limiter_isolates_different_ips(self):
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        limiter.is_rate_limited("10.0.0.1")
        limiter.is_rate_limited("10.0.0.1")

        # IP 10.0.0.1 deve ser bloqueado
        assert limiter.is_rate_limited("10.0.0.1")[0] is True

        # IP 10.0.0.2 deve ter acesso liberado
        assert limiter.is_rate_limited("10.0.0.2")[0] is False

    def test_rate_limiter_reset(self):
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        limiter.is_rate_limited("10.0.0.3")
        assert limiter.is_rate_limited("10.0.0.3")[0] is True

        limiter.reset()
        assert limiter.is_rate_limited("10.0.0.3")[0] is False
