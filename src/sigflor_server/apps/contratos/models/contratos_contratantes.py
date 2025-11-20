from django.db import models
from apps.comum.models import SoftDeleteModel
from apps.empresas.models import (
    Contratante,
    EmpresaCNPJ
    )

class ContratoContratante(SoftDeleteModel):
    numero_contrato_interno = models.CharField(
        max_length=20, unique=True, help_text='Numero do contrato internamente'
    )
    numero_contrato_contratante = models.CharField(
        max_length=50, blank=True, null=True, help_text='Numero do contrato no registro da contratante, para caso de integrações'
    )
    contratante_id = models.ForeignKey(
        Contratante, on_delete=models.PROTECT, related_name='contratos'
    )
    empresa_cnpj_id = models.ForeignKey(
        EmpresaCNPJ, on_delete=models.PROTECT, related_name='contratos_empresa_cnpj'
    )
    descricao = models.TextField(
        blank=True, null=True
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(
        blank=True, null=True
    )
    ativo = models.BooleanField(default=True)
    valor_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    class Meta:
        db_table = 'contratos_contratantes'
        verbose_name = 'Contrato Contratante'
        verbose_name_plural = 'Contratos Contratantes'
        constraints = [
            models.UniqueConstraint(
                fields=['numero_contrato_interno', 'contratante_id'],
                name='uniq_contrato_contratante_numero_interno_contratante'
            ),
            models.UniqueConstraint(
                fields=['numero_contrato_interno', 'contratante_id'],
                name='uniq_contrato_contratante_numero_contratante_contratante'
            ),
        ]