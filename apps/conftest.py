# =================================================================================

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.estoque.models import Pecas
import psycopg2
import pytest

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

@pytest.fixture(scope='session')
def db_ready():
    """Espera o PostgreSQL ficar pronto para aceitar conexões"""
    import time
    import os

    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 5432))
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')
    dbname = os.getenv('DB_NAME', 'postgres')

    conn = None
    for _ in range(30):
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=dbname
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            time.sleep(1)
    else:
        raise RuntimeError("PostgreSQL não ficou pronto a tempo")
    
# =================================================================================