# =================================================================================

from rest_framework import serializers
from .models import Pecas

# =================================================================================

class PecasSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Pecas.

    Converte instâncias do modelo Pecas em JSON e valida os dados recebidos
    da API.
    """

    class Meta:
        """
        Configuração do serializer.

        Atributos:
            model: Modelo associado ao serializer (Pecas).
            fields: Lista de campos a serem expostos na API.
            read_only_fields: Campos que não podem ser alterados via API.
        """
        model = Pecas
        fields = ['id', 'nome', 'descricao', 'preco', 'quantidade', 'criado_data', 'atualizado_data']
        read_only_fields = ['id', 'criado_data', 'atualizado_data']



    def validacao_preco(self, value):
        """
        Valida o campo 'preco'.

        Args:
            value (Decimal): Valor do preço enviado na requisição.

        Raises:
            serializers.ValidationError: Se o preço for negativo.

        Returns:
            Decimal: Valor do preço validado.
        """

        if value < 0:
            raise serializers.ValidationError("Preço não pode ser negativo!")
        return value

    def validacao_quantidade(self, value):
        """
        Valida o campo 'quantidade'.

        Args:
            value (int): Valor da quantidade enviado na requisição.

        Raises:
            serializers.ValidationError: Se a quantidade for negativa.

        Returns:
            int: Valor da quantidade validada.
        """

        if value < 0:
            raise serializers.ValidationError("Quantidade não pode ser negativa!")
        return value
    
# =================================================================================

