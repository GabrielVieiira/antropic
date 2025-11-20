from rest_framework import serializers
from apps.empresas.models import Filial
from apps.contatos.serializer import ContatoInSerializer, ContatoOutSerializer
from apps.enderecos.serializer import EnderecoInSerializer, EnderecoOutSerializer

class FilialInSerializer(serializers.ModelSerializer):
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir endereços repetidos e garantir que sempre tenha um principal.
    enderecos = EnderecoInSerializer(many=True, required=True)
    #Compensa utilizar o listserializer para aplicar regras unicas na lista? Tipo, não permitir contatos repetidos e garantir que sempre tenha um principal.
    contatos  = ContatoInSerializer(many=True, required=True)
    nome = serializers.CharField(max_length=150)
    #Provavelmente o código interno virá na requisição.
    codigo_interno = serializers.CharField(max_length=50, allow_null=True, allow_blank=True, required=False)
    #Vai ser no padrão de choices do Django ou de True ou false?
    status = serializers.ChoiceField(choices=Filial.STATUS_CHOICES, default='ativa')
    
    class Meta:
        model = Filial
        fields =['enderecos', 'contatos', 'nome', 'codigo_interno', 'status']

class FilialOutSerializer(serializers.ModelSerializer):
    enderecos = EnderecoOutSerializer(many=True, required=True)
    contatos  = ContatoOutSerializer(many=True, required=True)
    
    class Meta:
        model = Filial
        fields = ['id', 'created_at', 'updated_at', 'nome', 'codigo_interno', 'status', 'enderecos', 'contatos']
        read_only_fields = ['id', 'created_at', 'updated_at', 'enderecos', 'contatos']