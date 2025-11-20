from django.db import models
from apps.comum.models.base import SoftDeleteModel
from django.contrib.contenttypes.fields import GenericRelation

from apps.contatos.models import Contato
from apps.enderecos.models import Endereco
from apps.comum.managers.utils import validar_cnpj

class EmpresaCNPJ(SoftDeleteModel):
    razao_social = models.CharField(
        max_length=200,
        help_text="Razão social da empresa"
    )
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[validar_cnpj],
        help_text="CNPJ com 14 dígitos (apenas números)"
    )
    enderecos = GenericRelation(Endereco, related_query_name='empresa_cnpj')
    contatos = GenericRelation(Contato, related_query_name='empresa_cnpj')

    class Meta:
        db_table = 'empresa_cnpj'
        verbose_name = 'EmpresaCNPJ'
        verbose_name_plural = 'EmpresasCNPJ'
        constraints = [
            models.UniqueConstraint(
                fields=['razao_social'],
                name='uniq_empresa_cnpj_razao_social'
            ),
            models.UniqueConstraint(
                fields=['cnpj'],
                name='uniq_empresa_cnpj_cnpj'
            ),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        if self.cnpj:
            self.cnpj = ''.join(filter(str.isdigit, self.cnpj))
            validar_cnpj(self.cnpj)
        
        if self.razao_social:
            self.razao_social = self.razao_social.strip().title()

    def __str__(self):
        return f'{self.razao_social} ({self.cnpj_formatado})'
    
    @property 
    def cnpj_formatado(self):
        if len(self.cnpj) == 14:
            return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
        return self.cnpj