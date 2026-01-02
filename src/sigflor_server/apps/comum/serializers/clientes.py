from rest_framework import serializers

from ..models import Cliente, Empresa
from .pessoa_juridica import (
    PessoaJuridicaSerializer, 
    PessoaJuridicaCreateSerializer,
    PessoaJuridicaUpdateSerializer
)


class ClienteListSerializer(serializers.ModelSerializer):
    razao_social = serializers.ReadOnlyField()
    cnpj = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = [
            'id',
            'razao_social',
            'cnpj',
            'ativo',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

class ClienteSerializer(serializers.ModelSerializer):

    pessoa_juridica = PessoaJuridicaSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'pessoa_juridica',
            'descricao',
            'ativo',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = [
            'id', 'razao_social', 'nome_fantasia', 'cnpj', 'cnpj_formatado',
            'created_at', 'updated_at'
        ]

class ClienteCreateSerializer(serializers.ModelSerializer):

    pessoa_juridica = PessoaJuridicaCreateSerializer(required=True)
    empresa_gestora = serializers.PrimaryKeyRelatedField(required=True, queryset=Empresa.objects.all())
    class Meta:
        model = Cliente
        fields = [
            'pessoa_juridica',
            'descricao',
            'empresa_gestora',
            'ativo',
        ]

class ClienteUpdateSerializer(serializers.ModelSerializer):

    pessoa_juridica = PessoaJuridicaUpdateSerializer(required=False)
    
    class Meta:
        model = Cliente
        fields = [
            'pessoa_juridica',
            'descricao',
            'empresa_gestora',
            'ativo',
        ]

class ClienteSelectionSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='pessoa_juridica.razao_social', read_only=True)
    cnpj = serializers.CharField(source='pessoa_juridica.cnpj_formatado', read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'label', 'cnpj']