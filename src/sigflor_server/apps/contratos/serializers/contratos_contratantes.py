from rest_framework import serializers
from apps.contratos.models import ContratoContratante

class ContratoContratanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoContratante
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        if data['data_fim'] and data['data_fim'] < data['data_inicio']:
            raise serializers.ValidationError("Data de fim não pode ser anterior à data de início.")
        return data