from rest_framework import serializers

from ..models import Permissao


class PermissaoSerializer(serializers.ModelSerializer):
    """Serializer para Permissão."""

    class Meta:
        model = Permissao
        fields = [
            'id',
            'codigo',
            'nome',
            'descricao',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']



