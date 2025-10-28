# =================================================================================

from celery import shared_task
from .models import Pecas
import csv
import io
import logging

logger = logging.getLogger('apps.estoque')

# =================================================================================

@shared_task
def celery_csv(csv_conteudo):
    """
    Processa o conteúdo CSV e cria ou atualiza registros de peças.

    Args:
        csv_conteudo (str): Conteúdo do arquivo CSV, já decodificado em texto.

    Returns:
        int: Número de linhas processadas com sucesso.

    Raises:
        Exception: Em caso de erro de parsing ou inconsistência nos dados.

    Observações:
        - Usa update_or_create() para evitar duplicação de peças.
        - Campos esperados: nome, descricao, preco, quantidade.
    """

    try:
        leitor = csv.DictReader(io.StringIO(csv_conteudo))
        count = 0

        for linha in leitor:
            try:
                preco = float(linha.get('preco', 0))
            except:
                preco = 0.0

            try:
                quantidade = int(linha.get('quantidade', 0))
            except:
                quantidade = 0

            nome = linha.get('nome')

            logger.debug(f"Processando: {nome} | Qtnd: {quantidade} | Valor: {preco}")

            Pecas.objects.update_or_create(
                nome=nome,
                defaults={
                    'descricao': linha.get('descricao', ''),
                    'preco': preco,
                    'quantidade': quantidade,
                },
            )
            count += 1

        logger.info(f"[Celery CSV] Importação finalizada, {count} peças carregadas.")
        return count

    except Exception as e:
        logger.exception(f"[Celery CSV] Erro ao processar CSV: {e}")
        raise e

# =================================================================================

@shared_task
def repor_estoque(qnt_min=10):
    """
        Reposição automática de estoque para todas as peças abaixo do mínimo.

        Args:
            qnt_min (int): Quantidade mínima desejada por peça (default=10).

        Returns:
            str: Mensagem com número de peças atualizadas.
    """
    
    try:
        pecas_repor = Pecas.objects.filter(quantidade__lt=qnt_min)
        total = pecas_repor.count()

        for peca in pecas_repor:

            logger.debug(f"Reposição Auto - {peca.nome}: {peca.quantidade} - {qnt_min}")

            peca.quantidade = qnt_min
            peca.save()

        logger.info(f"[Celery CRON] {total} peças repostas.")

        return f"{pecas_repor.count()} peças atualizadas."
    
    except Exception as e:
        logger.exception(f"[Celery CRON] Erro ao repor estoque: {e}")
        raise e
    
# =================================================================================
