from rest_framework import serializers
from apps.autenticacao.serializers import UsuarioResumoSerializer
from ..models import Exame

class ExameSerializer(serializers.ModelSerializer):

    created_by = UsuarioResumoSerializer()
    updated_by = UsuarioResumoSerializer()

    class Meta:
        model = Exame
        fields = [
            'id', 
            'nome', 
            'descricao', 
            'created_at', 
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

class ExameSelecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = ['id', 'nome']