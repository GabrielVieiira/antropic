import uuid
from django.db import models
from apps.comum.models.base import SoftDeleteModel


class Exame(SoftDeleteModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Exame")
    descricao = models.TextField(blank=True, default='', verbose_name="Descrição do Exame")
    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
        ]

    def __str__(self):
        return self.nome
