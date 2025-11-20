from rest_framework import serializers
from apps.empresas.models import Contratante
from apps.contatos.serializer import ContatoInSerializer, ContatoOutSerializer
from apps.enderecos.serializer import EnderecoInSerializer, EnderecoOutSerializer

class ContratanteInSerializer(serializers.ModelSerializer):
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir endereços repetidos e garantir que sempre tenha um principal.
    enderecos = EnderecoInSerializer(many=True, required=True)
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir contatos repetidos e garantir que sempre tenha um principal.
    contatos  = ContatoInSerializer(many=True, required=True)
    nome = serializers.CharField(max_length=200)
    cnpj = serializers.CharField(max_length=14)
    descricao = serializers.CharField(allow_blank=True, allow_null=True, required=True)
    #Vai ser no padrão de choices do Django ou de True ou false?
    ativo = serializers.BooleanField(default=True)
    
    class Meta:
        model = Contratante
        fields = ['enderecos', 'contatos', 'nome', 'cnpj', 'descricao', 'ativo']

    def validate_nome(self, value:str) -> str:
        return value.upper()

class ContratanteOutSerializer(serializers.ModelSerializer):
    enderecos = EnderecoOutSerializer(many=True, required=True)
    contatos  = ContatoOutSerializer(many=True, required=True)
    
    class Meta:
        model = Contratante
        fields = ['id', 'created_at', 'updated_at', 'nome', 'cnpj', 'descricao', 'ativo', 'enderecos', 'contatos']
        read_only_fields = ['id', 'created_at', 'updated_at', 'enderecos', 'contatos']
