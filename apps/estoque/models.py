# =================================================================================

from django.db import models

# =================================================================================

class Pecas(models.Model):
    """
    Modelo que representa uma peça de autopeça no estoque.

    Attributes:
        nome (str): Nome da peça.
        descricao (str): Descrição da peça (opcional).
        quantidade (int): Quantidade disponível no estoque.
        preco (Decimal): Preço da peça.
        criado_data (datetime): Data de criação do registro (automático, criado pelo django).
        atualizado_data (datetime): Data da última atualização do registro (automático, criado pelo django).
    """

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    quantidade = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=15, decimal_places=2)

    criado_data = models.DateTimeField(auto_now_add=True)
    atualizado_data = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.nome} ({self.quantidade} unds) - R$ {self.preco}"
    
# =================================================================================