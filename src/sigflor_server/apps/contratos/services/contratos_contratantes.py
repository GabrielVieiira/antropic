from apps.contratos.models import ContratoContratante
from django.db import transaction

class ContratoContratanteService:
    @transaction.atomic
    def criar_contrato_contratante(data):
        contrato = ContratoContratante(**data)
        contrato.full_clean()
        contrato.save()
        return contrato

    @transaction.atomic
    def atualizar_contrato_contratante(contrato: ContratoContratante, data: dict):
        for campo, valor in data.items():
            setattr(contrato, campo, valor)
        contrato.full_clean()
        contrato.save()
        return contrato