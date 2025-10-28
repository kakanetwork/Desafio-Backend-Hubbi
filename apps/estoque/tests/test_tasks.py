# =================================================================================

import pytest
from apps.estoque.models import Pecas
from apps.estoque.tasks import repor_estoque, celery_csv

# =================================================================================

pytestmark = pytest.mark.django_db

# =================================================================================

def test_repor_estoque_task():
    """
    Cria peças com quantidade baixa e executa repor_estoque() diretamente.
    Verifica se o comportamento de ajuste para 10 unidades funciona.
    """
    Pecas.objects.create(nome="Filtro", descricao="x", preco=10.0, quantidade=5)
    Pecas.objects.create(nome="Freio", descricao="x", preco=50.0, quantidade=12)

    result = repor_estoque(10)  # chama a função )()
    # Checar que a peça com 5 passou para 10
    assert Pecas.objects.get(nome="Filtro").quantidade == 10
    assert Pecas.objects.get(nome="Freio").quantidade == 12
    assert "1 peças" in result or "1 peça" in result

# =================================================================================

def test_celery_csv_creates_or_updates():
    """
    Executa celery_csv diretamente com conteúdo CSV e verifica criação/atualização.
    """
    csv_data = "nome,descricao,preco,quantidade\nVelas,NGK,25.00,15\nParafuso,Standard,1.50,40"
    celery_csv(csv_data)
    assert Pecas.objects.filter(nome="Velas").exists()
    assert Pecas.objects.filter(nome="Parafuso").exists()

    csv_data_update = "nome,descricao,preco,quantidade\nVelas,NGK-updated,30.00,20"
    celery_csv(csv_data_update)
    velas = Pecas.objects.get(nome="Velas")
    assert velas.descricao == "NGK-updated"
    assert float(velas.preco) == 30.00
    assert velas.quantidade == 20

# =================================================================================
