from django.db import models
from apps.comum.models.base import SoftDeleteModel
from django.contrib.contenttypes.fields import GenericRelation

from apps.contatos.models import Contato
from apps.enderecos.models import Endereco
from apps.comum.managers.utils import validar_cnpj

class Contratante(SoftDeleteModel):
    nome = models.CharField(
        max_length=200,
        help_text="Nome do contratante"
        )
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[validar_cnpj],
        help_text="CNPJ com 14 dígitos (apenas números)"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        help_text="Descrição adicional sobre o contratante"
        )
    #Vai ser no padrão de choices (enum) ou de True ou false?
    ativo = models.BooleanField(
        default=True,
        help_text="Indica se o contratante está ativo"
        )
    enderecos = GenericRelation(Endereco, related_query_name='contratantes')
    contatos = GenericRelation(Contato, related_query_name='contratantes')

    class Meta:
        db_table = 'contratantes'
        verbose_name = 'Contratante'
        verbose_name_plural = 'Contratantes'
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'cnpj'],
                name='uniq_contratantes_nome_cnpj'
            )
        ]

    def __str__(self):
        return f'{self.nome} ({self.cnpj})'

    @property 
    def cnpj_formatado(self):
        if len(self.cnpj) == 14:
            return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
        return self.cnpj