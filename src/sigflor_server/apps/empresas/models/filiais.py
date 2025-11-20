from django.db import models
from apps.comum.models.base import SoftDeleteModel
from django.contrib.contenttypes.fields import GenericRelation

from apps.contatos.models import Contato
from apps.enderecos.models import Endereco

class Filial(SoftDeleteModel):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('inativa', 'Inativa'),
        ('suspensa', 'Suspensa'),
    ]

    nome = models.CharField(max_length=150)
    codigo_interno = models.CharField(max_length=50)
    #Vai ser no padrão de choices (enum) ou de True ou false?
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    enderecos = GenericRelation(Endereco, related_query_name='filiais')
    contatos = GenericRelation(Contato, related_query_name='filiais')

    class Meta:
        db_table = 'filiais'
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'

    def __str__(self):
        return self.nome