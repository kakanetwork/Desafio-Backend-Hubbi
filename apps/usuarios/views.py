# =================================================================================

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets
import logging

logger = logging.getLogger('apps.usuarios')

# =================================================================================

class UsuariosView(viewsets.ReadOnlyModelViewSet):
    """
    View para listar usuários.

    Apenas admins podem listar.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        logger.info(f"O Admin: '{request.user.username}' - listou todos os usuários.")
        return super().list(request, *args, **kwargs)


# =================================================================================
