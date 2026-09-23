"""
Configuração e Fixtures Globais do Pytest.
"""

import pytest
from fastapi.testclient import TestClient

from src.core.security import rate_limiter
from src.main import app


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reseta o rate limiter antes de cada teste para garantir isolamento."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()


@pytest.fixture
def client():
    """Fixture que fornece um TestClient FastAPI para testes de integração."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Cabeçalhos com API Key válida para testes de rotas protegidas."""
    return {"X-API-Key": "soap-secret-key-2026"}


@pytest.fixture
def bearer_headers():
    """Cabeçalhos com Bearer Token válido para testes de autenticação."""
    return {"Authorization": "Bearer soap-secret-key-2026"}


@pytest.fixture
def sample_viacep_response():
    """Mock de resposta válida do ViaCEP."""
    return {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107",
    }
