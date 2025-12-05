# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Filial
from ..serializers.enderecos import FilialEnderecoNestedSerializer, FilialEnderecoListSerializer
from ..serializers.contatos import FilialContatoNestedSerializer, FilialContatoListSerializer
from ..models.enums import StatusFilial


class FilialSerializer(serializers.ModelSerializer):

    is_ativa = serializers.ReadOnlyField()
    empresa_nome = serializers.ReadOnlyField()
    enderecos = FilialEnderecoListSerializer(many=True, read_only=True, source='enderecos_vinculados')
    contatos = FilialContatoListSerializer(many=True, read_only=True, source='contatos_vinculados')

    class Meta:
        model = Filial
        fields = [
            'id',
            'nome',
            'enderecos',
            'contatos',
            'codigo_interno',
            'status',
            'descricao',
            'empresa',
            'empresa_nome',
            'is_ativa',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_ativa', 'created_at', 'updated_at']

class FilialCreateSerializer(serializers.ModelSerializer):
    
    enderecos = FilialEnderecoNestedSerializer(many=True, required=True, allow_empty=False)
    contatos = FilialContatoNestedSerializer(many=True, required=True, allow_empty=False)

    class Meta:
        model = Filial
        fields = [
            'nome',
            'codigo_interno',
            'status',
            'descricao',
            'empresa',
            'contatos',
            'enderecos',
        ]
        extra_kwargs = {
            'status': {'choices': StatusFilial.choices}
        }

class FilialListSerializer(serializers.ModelSerializer):

    empresa_nome = serializers.ReadOnlyField()

    class Meta:
        model = Filial
        fields = [
            'id',
            'nome',
            'codigo_interno',
            'status',
            'empresa_nome',
        ]
