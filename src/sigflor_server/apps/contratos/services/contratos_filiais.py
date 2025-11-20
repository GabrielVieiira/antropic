from apps.contratos.models import ContratoFiliais
from django.db import transaction

class ContratoFiliaisService:
    @transaction.atomic
    def criar_contrato_filial(data):
        subcontrato = ContratoFiliais(**data)
        subcontrato.full_clean()
        subcontrato.save()
        return subcontrato

    @transaction.atomic
    def atualizar_contrato_filial(subcontrato: ContratoFiliais, data: dict):
        for campo, valor in data.items():
            setattr(subcontrato, campo, valor)
        subcontrato.full_clean()
        subcontrato.save()
        return subcontrato