from rest_framework import serializers
from apps.contratos.models import ContratoFiliais

class ContratoFiliaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoFiliais
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        contrato = data['contrato']
        filial = data['filial']
        existe = ContratoFiliais.objects.filter(contrato=contrato, filial=filial).exists()
        if existe:
            raise serializers.ValidationError("Já existe um subcontrato para essa filial nesse contrato.")
        return data