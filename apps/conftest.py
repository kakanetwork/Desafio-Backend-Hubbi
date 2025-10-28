# =================================================================================

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.estoque.models import Pecas

# =================================================================================

@pytest.fixture
def api_client():
    """Retorna um REST framework APIClient sem autenticação."""
    return APIClient()

# =================================================================================

@pytest.fixture
def admin_user(db):
    """Cria e retorna um superuser para testes."""
    return User.objects.create_superuser(username='admin', email='admin@example.com', password='123456')

# =================================================================================

@pytest.fixture
def regular_user(db):
    """Cria e retorna um usuário comum para testes."""
    return User.objects.create_user(username='user', email='user@example.com', password='123456')

# =================================================================================

@pytest.fixture
def peca_exemplo(db):
    """Cria uma peça de exemplo no banco."""
    return Pecas.objects.create(nome="Filtro de óleo", descricao="Filtro padrão", preco=50.0, quantidade=5)

# =================================================================================
