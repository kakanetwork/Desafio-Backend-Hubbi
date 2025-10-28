# =================================================================================

import pytest
from django.urls import reverse
from rest_framework import status

# =================================================================================

pytestmark = pytest.mark.django_db

# =================================================================================

def test_list_users_admin(api_client, admin_user):
    """
    Apenas usuário admin pode listar usuários.
    """
    api_client.force_authenticate(user=admin_user)
    url = reverse('usuarios-list')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.data, list)


def test_list_users_non_admin_forbidden(api_client, regular_user):
    """
    Usuário comum não pode listar usuários (403).
    """
    api_client.force_authenticate(user=regular_user)
    url = reverse('usuarios-list')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

# =================================================================================
