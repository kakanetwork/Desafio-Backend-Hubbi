# =================================================================================

from rest_framework import serializers
from .models import Pecas
import mimetypes

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



    def validate_preco(self, value):
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

    def validate_quantidade(self, value):
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

class CSVSerializer(serializers.Serializer):
    """
    Serializer dos arquivos CSV enviados via API.

    Campos:
        file (FileField): Arquivo enviado pelo usuário.

    Validações:
        - O arquivo deve ter extensão .csv.
        - O arquivo deve ter MIME type -> text/csv ou application/vnd.ms-excel.
    
    Obs:
        MIME Type é um identificador padrão de formato dos arquivos, estamos utilizando a Bib mimetypes para fazer essa verificação.
    """

    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("O arquivo deve ser .csv")

        mime, _ = mimetypes.guess_type(value.name)
        value.seek(0)  # Volta o ponteiro do arquivo para o início
        if mime != 'text/csv' and mime != 'application/vnd.ms-excel': # o Tipo CSV/XLSX/XLS pode ter esses dois MIME types
            # Ref: https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Guides/MIME_types/Common_types
            raise serializers.ValidationError("Arquivo inválido. Esperado CSV.")
        
        return value

# =================================================================================
