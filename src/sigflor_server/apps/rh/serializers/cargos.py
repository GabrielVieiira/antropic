from rest_framework import serializers

from ..models import Cargo
from ..models.enums import NivelCargo
from .cargo_documento import CargoDocumentoNestedSerializer


class CargoListSerializer(serializers.ModelSerializer):
    funcionarios_count = serializers.ReadOnlyField()
    tem_risco = serializers.ReadOnlyField()

    class Meta:
        model = Cargo
        fields = [
            'id',
            'nome',
            'cbo',
            'nivel',
            'salario_base',
            'ativo',
            'tem_risco',
            'funcionarios_count',
        ]

class CargoSerializer(serializers.ModelSerializer):
    funcionarios_count = serializers.ReadOnlyField()
    tem_risco = serializers.ReadOnlyField()
    documentos_obrigatorios = CargoDocumentoNestedSerializer(
        many=True, 
        read_only=True, 
        source='documentos_obrigatorios'
    )

    class Meta:
        model = Cargo
        fields = [
            'id',
            'nome',
            'cbo',
            'descricao',
            'salario_base',
            'nivel',
            'risco_fisico',
            'risco_biologico',
            'risco_quimico',
            'risco_ergonomico',
            'risco_acidente',
            'tem_risco',
            'ativo',
            'documentos_obrigatorios',
            'funcionarios_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'funcionarios_count', 'tem_risco',
            'created_at', 'updated_at'
        ]

class CargoCreateSerializer(serializers.ModelSerializer):
    documentos = CargoDocumentoNestedSerializer(many=True, required=False)

    class Meta:
        model = Cargo
        fields = [
            'nome',
            'cbo',
            'descricao',
            'salario_base',
            'nivel',
            'risco_fisico',
            'risco_biologico',
            'risco_quimico',
            'risco_ergonomico',
            'risco_acidente',
            'ativo',
            'documentos',
        ]
        extra_kwargs = {
            'nivel': {'choices': NivelCargo.choices},
        }

    def validate_documentos(self, value):
        tipos_vistos = set()
        for item in value:
            tipo = item.get('documento_tipo')
            if tipo in tipos_vistos:
                raise serializers.ValidationError(
                    f"O documento '{tipo}' foi informado mais de uma vez."
                )
            tipos_vistos.add(tipo)
        return value

class CargoUpdateSerializer(serializers.ModelSerializer):
    documentos = CargoDocumentoNestedSerializer(many=True, required=False)

    class Meta:
        model = Cargo
        fields = [
            'nome',
            'cbo',
            'descricao',
            'salario_base',
            'nivel',
            'risco_fisico',
            'risco_biologico',
            'risco_quimico',
            'risco_ergonomico',
            'risco_acidente',
            'ativo',
            'documentos',
        ]
        extra_kwargs = {
            'nivel': {'choices': NivelCargo.choices},
        }

class CargoSelecaoSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='nome', read_only=True)
    
    class Meta:
        model = Cargo
        fields = ['id', 'label', 'cbo']