"""
Testes Unitários do Módulo de Segurança (security.py).
"""

import pytest

from src.core.security import (
    RateLimiter,
    sanitize_input,
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
