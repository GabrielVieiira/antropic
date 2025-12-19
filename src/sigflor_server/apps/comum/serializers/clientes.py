from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from ..models import Cliente, Empresa
from .pessoa_juridica import (
    PessoaJuridicaSerializer, 
    PessoaJuridicaCreateSerializer, 
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
            'descricao',
            'ativo',
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