from rest_framework import serializers
from .models import Contato

class ContatoInSerializer(serializers.ModelSerializer):
    tipo            = serializers.ChoiceField(choices=Contato.Tipo.choices)
    valor           = serializers.CharField(max_length=150, trim_whitespace=True)
    principal       = serializers.BooleanField(required=False, default=False)

    class Meta:
        model   = Contato
        fields  = [
            'tipo', 'valor', 'principal',
        ]

class ContatoOutSerializer(serializers.ModelSerializer):
    id =                serializers.IntegerField(read_only=True)
    valor_formatado =   serializers.CharField(read_only=True)
    tipo =              serializers.ChoiceField(choices=Contato.Tipo.choices, read_only=True)
    valor =             serializers.CharField(read_only=True)
    principal =         serializers.BooleanField(read_only=True)
    created_at =        serializers.DateTimeField(read_only=True)
    updated_at =        serializers.DateTimeField(read_only=True)
    deleted_at =        serializers.DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model   = Contato
        fields  = [
            'id', 'tipo',
            'valor', 'valor_formatado',
            'principal', 'created_at', 
            'updated_at', 'deleted_at',
        ]
