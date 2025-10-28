# =================================================================================

from django.contrib import admin
from .models import Pecas

# =================================================================================

@admin.register(Pecas)
class PecasAdmin(admin.ModelAdmin):
    """
    Configuração da interface admin para o modelo dePecas.
    """
    list_display = ('nome', 'quantidade', 'preco', 'criado_data', 'atualizado_data')
    list_filter = ('quantidade', 'criado_data')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

# =================================================================================