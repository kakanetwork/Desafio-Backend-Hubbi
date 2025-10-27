# =================================================================================

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PecasSerializer
from .serializers import CSVSerializer
from rest_framework import viewsets
from rest_framework import status
from .tasks import celery_csv
from .models import Pecas

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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    queryset = Pecas.objects.all()
    serializer_class = PecasSerializer

# =================================================================================

class CSVView(APIView):
    """
    Endpoint para upload de planilha CSV de peças.

    Apenas admins podem enviar arquivos.
    """

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = CSVSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data['file']

            # Chama a task do Celery de forma assíncrona
            celery_csv.delay(file.read().decode('utf-8'))
            
            return Response({"message": "Arquivo recebido. Processamento iniciado."}, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# =================================================================================
