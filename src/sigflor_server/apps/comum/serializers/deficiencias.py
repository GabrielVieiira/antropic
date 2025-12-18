# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Deficiencia


class DeficienciaSerializer(serializers.ModelSerializer):

    pessoa_fisica_nome = serializers.CharField(
        source='pessoa_fisica.nome_completo',
        read_only=True
    )
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )

    class Meta:
        model = Deficiencia
        fields = [
            'id',
            'pessoa_fisica',
            'pessoa_fisica_nome',
            'nome',
            'tipo',
            'tipo_display',
            'cid',
            'grau',
            'congenita',
            'observacoes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeficienciaNestedSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(required=False)
    
    class Meta:
        model = Deficiencia
        fields = [
            'id',
            'nome',
            'tipo',
            'cid',
            'grau',
            'congenita',
            'observacoes',
        ]


class DeficienciaListSerializer(serializers.ModelSerializer):

    pessoa_fisica_nome = serializers.CharField(
        source='pessoa_fisica.nome_completo',
        read_only=True
    )
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )

    class Meta:
        model = Deficiencia
        fields = [
            'id',
            'pessoa_fisica',
            'pessoa_fisica_nome',
            'nome',
            'tipo',
            'tipo_display',
            'cid',
            'congenita',
        ]

