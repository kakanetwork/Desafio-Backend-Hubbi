# =================================================================================

from apps.estoque.tasks import repor_estoque, celery_csv
from apps.estoque.models import Pecas
from rest_framework import status
from django.urls import reverse
import pytest
import io

# =================================================================================

pytestmark = pytest.mark.django_db

# =================================================================================

def test_celery_repor_estoque_task_real():
    Pecas.objects.create(nome="Filtro", descricao="x", preco=10.0, quantidade=5)

    task = repor_estoque.delay(10)
    result = task.get(timeout=10)  # Espera o worker processar
    pecas = Pecas.objects.get(nome="Filtro")
    assert pecas.quantidade == 10
    assert "1 peças" in result or "1 peça" in result

# =================================================================================

def test_celery_csv_task_real():
    csv_data = "nome,descricao,preco,quantidade\nVelas,NGK,25.00,15"
    task = celery_csv.delay(csv_data)
    task.get(timeout=10)  # Espera o Celery processar

    assert Pecas.objects.filter(nome="Velas").exists()

# =================================================================================

def test_csv_upload_full_flow(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('upload_csv')
    csv_content = "nome,descricao,preco,quantidade\nFiltro,Filtro de ar,30,15"
    file_obj = io.BytesIO(csv_content.encode('utf-8'))
    file_obj.name = 'pecas.csv'

    # envia arquivo para endpoint
    resp = api_client.post(url, {'file': file_obj}, format='multipart')
    assert resp.status_code == status.HTTP_202_ACCEPTED

    # Espera o Celery processar
    celery_csv(file_obj.getvalue().decode())

    assert Pecas.objects.filter(nome="Filtro").exists()

# =================================================================================
