from rest_framework import serializers
from apps.empresas.models import EmpresaCNPJ
from apps.contatos.serializer import ContatoInSerializer, ContatoOutSerializer
from apps.enderecos.serializer import EnderecoInSerializer, EnderecoOutSerializer

class EmpresaCNPJInSerializer(serializers.ModelSerializer):
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir endereços repetidos e garantir que sempre tenha um principal.
    enderecos = EnderecoInSerializer(many=True, required=True)
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir contatos repetidos e garantir que sempre tenha um principal.
    contatos  = ContatoInSerializer(many=True, required=True)
    class Meta:
        model  = EmpresaCNPJ
        fields = ['razao_social', 'cnpj', 'enderecos', 'contatos']

class EmpresaCNPJOutSerializer(serializers.ModelSerializer):
    enderecos = EnderecoOutSerializer(many=True, required=True)
    contatos  = ContatoOutSerializer(many=True, required=True)

    class Meta:
        model  = EmpresaCNPJ
        fields = ['id', 'created_at', 'updated_at', 'razao_social', 'cnpj', 'cnpj_formatado', 'enderecos', 'contatos']
        read_only_fields = ['id', 'created_at', 'updated_at', 'razao_social', 'cnpj', 'enderecos', 'contatos', 'cnpj_formatado']
