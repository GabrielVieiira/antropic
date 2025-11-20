from django.db import models
from apps.comum.models import SoftDeleteModel
from apps.empresas.models import (
    Filial,
    )
from . import ContratoContratante
from apps.empresas.models.filiais import Filial

class ContratoFiliais(SoftDeleteModel):
    numero = models.CharField(
        max_length=20, unique=True, help_text='Identificador unico do contrato'
        )
    filial_id = models.ForeignKey(Filial, on_delete=models.PROTECT, related_name='contratos')
    contrato_id = models.ForeignKey(ContratoContratante, on_delete=models.PROTECT, related_name='filiais_contrato')
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'contratos_filiais'
        verbose_name = 'Contrato Filial'
        verbose_name_plural = 'Contratos Filiais'
        constraints = [
            models.UniqueConstraint(
                fields=['numero', 'filial_id'],
                name='uniq_contrato_filial_numero_filial'
            ),
            models.UniqueConstraint(
                fields=['contrato_id', 'numero'],
                name='uniq_contrato_filial_contrato_numero'
            ),
        ]