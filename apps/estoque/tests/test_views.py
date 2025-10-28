# =================================================================================

import io
import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from apps.estoque.models import Pecas

# =================================================================================

pytestmark = pytest.mark.django_db

# =================================================================================


def test_list_pecas_authenticated(api_client, admin_user, peca_exemplo):
    """
    Usuário autenticado deve conseguir listar peças (200).
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('pecas-list')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.data, list)
    assert resp.data[0]['nome'] == peca_exemplo.nome

# =================================================================================

def test_retrieve_peca_detail(api_client, admin_user, peca_exemplo):
    """
    Recuperar detalhe de peça por id.
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('pecas-detail', args=[peca_exemplo.id])
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['id'] == peca_exemplo.id

# =================================================================================

def test_create_peca_admin(api_client, admin_user):
    """
    Apenas admin pode criar peça (201).
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('pecas-list')
    payload = {
        "nome": "Amortecedor",
        "descricao": "Amortecedor dianteiro",
        "preco": 120.0,
        "quantidade": 10
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    assert Pecas.objects.filter(nome="Amortecedor").exists()

# =================================================================================

def test_create_peca_non_admin_forbidden(api_client, regular_user):
    """
    Usuário comum não pode criar peça (403).
    """
    api_client.force_authenticate(user=regular_user)
    url = reverse('pecas-list')
    payload = {
        "nome": "Amortecedor",
        "descricao": "Amortecedor dianteiro",
        "preco": 120.0,
        "quantidade": 10
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

# =================================================================================

def test_update_peca_admin(api_client, admin_user, peca_exemplo):
    """
    Admin consegue atualizar (PATCH) uma peça.
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('pecas-detail', args=[peca_exemplo.id])
    resp = api_client.patch(url, {'preco': 60.0}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    peca_exemplo.refresh_from_db()
    assert float(peca_exemplo.preco) == 60.0

# =================================================================================

def test_delete_peca_admin(api_client, admin_user, peca_exemplo):
    """
    Admin consegue deletar peça (204).
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('pecas-detail', args=[peca_exemplo.id])
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert not Pecas.objects.filter(id=peca_exemplo.id).exists()

# =================================================================================

@patch('apps.estoque.views.celery_csv.delay')
def test_upload_csv_admin(mock_delay, api_client, admin_user):
    """
    Upload CSV por admin deve agendar a task Celery (202). 
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('upload_csv')
    csv_content = "nome,descricao,preco,quantidade\nFiltro,Filtro de ar,30,15"
    file_obj = io.BytesIO(csv_content.encode('utf-8'))
    file_obj.name = 'pecas.csv'

    resp = api_client.post(url, {'file': file_obj}, format='multipart')
    assert resp.status_code == status.HTTP_202_ACCEPTED
    # .delay deve ser chamada com o conteúdo (string)
    assert mock_delay.call_count == 1

# =================================================================================

def test_upload_csv_non_admin_forbidden(api_client, regular_user):
    """
    Upload CSV por usuário comum deve retornar 403.
    """
    api_client.force_authenticate(user=regular_user)
    url = reverse('upload_csv')
    csv_content = "nome,descricao,preco,quantidade\nFiltro,Filtro de ar,30,15"
    file_obj = io.BytesIO(csv_content.encode('utf-8'))
    file_obj.name = 'pecas.csv'

    resp = api_client.post(url, {'file': file_obj}, format='multipart')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

# =================================================================================
