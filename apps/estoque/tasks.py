# =================================================================================

from celery import shared_task
from .models import Pecas
import csv
import io

# =================================================================================

@shared_task
def celery_csv(csv_content):
    """
    Processa o CSV das peças e cria/atualiza no banco.
    """

    leitor = csv.DictReader(io.StringIO(csv_content))

    for linha in leitor:
        Pecas.objects.update_or_create(
            nome=linha['nome'],
            defaults={
                'descricao': linha.get('descricao', ''),
                'preco': linha.get('preco', 0),
                'quantidade': linha.get('quantidade', 0)
            }
        )

# =================================================================================
