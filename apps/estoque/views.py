# =================================================================================

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PecasSerializer
from .serializers import CSVSerializer
from rest_framework import viewsets
from rest_framework import status
from .tasks import celery_csv
from .models import Pecas
import logging

logger = logging.getLogger('apps.estoque')

# =================================================================================

class PecasView(viewsets.ModelViewSet):
    """
    View que vai gerenciar/backend do módulo de peças do marketplace.

    Funcionalidades:
        - Listar todas as peças (qualquer usuário autenticado)
        - Visualizar detalhes de uma peça
        - Criar, atualizar e deletar peças (apenas admin)
    """

    def get_permissions(self):
        """Define permissões dinamicamente por tipo de ação."""

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Loga criação de nova peça."""
        instance = serializer.save()
        logger.info(f"Nova peça: {instance.nome}")

    def perform_destroy(self, instance):
        """Loga exclusão de peça."""
        logger.warning(f"Peça excluída: {instance.nome}")
        instance.delete()

    queryset = Pecas.objects.all()
    serializer_class = PecasSerializer

# =================================================================================

class CSVView(APIView):
    """
    Endpoint para upload de planilha CSV de peças.
    Apenas usuários admin podem enviar arquivos.

    Funcionalidade:
        - Recebe um arquivo CSV com colunas: nome, descricao, preco, quantidade
        - Processa o CSV de forma assíncrona via Celery
    """

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser]  

    def post(self, request, *args, **kwargs):
        """
        Recebe e valida um arquivo CSV.
        A importação é processada em background por Celery.
        """

        serializer = CSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data['file']
        csv_content = csv_file.read().decode('utf-8')

        logger.info(f"Arquivo CSV recebido: {csv_file.name}")
        celery_csv.delay(csv_content)
        logger.info(f"Tarefa Celery criada para: {csv_file.name}")

        return Response(
            {
                "detail": "Importação agendada com sucesso.",
                "message": "O arquivo foi recebido e está sendo processado em background.",
            },
            status=status.HTTP_202_ACCEPTED,
        )
    
# =================================================================================
