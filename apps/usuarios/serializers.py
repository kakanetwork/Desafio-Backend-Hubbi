
# =================================================================================

from django.contrib.auth.models import User
from rest_framework import serializers

# =================================================================================

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo de usuário padrão do Django -> "User".

    Este serializer é usado para expor dados de usuários via API
    e para manipular usuários (ex.: listagem, detalhes ou criação de perfis).

    Obs:
        - Não criei um modelo custom de usuário, já que o modelo
          padrão do Django forneceu todos os campos que precisamos.
        - Campos como `is_staff` são definidos como read-only para evitar
          que usuários comuns possam se tornar administradores via API.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = ['id', 'is_staff']

# =================================================================================
