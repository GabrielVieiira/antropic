from multiprocessing import allow_connection_pickling
from rest_framework import serializers
from .models import Endereco

class EnderecoInSerializer(serializers.Serializer):
    id             = serializers.IntegerField(required=False, allow_null=True)
    logradouro      = serializers.CharField(max_length=200)
    numero          = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    complemento     = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    bairro          = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    cidade          = serializers.CharField(max_length=100)
    estado          = serializers.CharField(max_length=2)
    cep             = serializers.CharField(max_length=8)
    pais            = serializers.CharField(max_length=50, required=False, default="Brasil")
    principal       = serializers.BooleanField(required=False, default=False)
    class Meta:
        model = Endereco
        fields = [
            'logradouro', 'numero',
            'complemento', 'bairro', 
            'cidade', 'estado', 'cep', 
            'pais', 'principal', 'content_type', 
            'object_id', 'deleted_at', 'id'
            ]

class EnderecoOutSerializer(serializers.Serializer):
    id         = serializers.IntegerField()
    logradouro = serializers.CharField()
    numero     = serializers.CharField(allow_null=True, allow_blank=True)
    complemento= serializers.CharField(allow_null=True, allow_blank=True)
    bairro     = serializers.CharField(allow_null=True, allow_blank=True)
    cidade     = serializers.CharField()
    estado     = serializers.CharField()
    cep        = serializers.CharField()
    pais       = serializers.CharField()
    principal  = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    deleted_at = serializers.DateTimeField(allow_null=True)
    class Meta:
        model = Endereco
        fields = [
            'id', 'logradouro', 'numero', 
            'complemento', 'bairro', 
            'cidade', 'estado', 'cep', 
            'pais', 'principal', 'created_at', 
            'updated_at', 'deleted_at'
            ]
        read_only_fields = [
            'id', 'logradouro', 
            'numero', 'complemento', 
            'bairro', 'cidade', 
            'estado', 'cep', 'pais'
            ]
