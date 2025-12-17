import uuid
from django.db import models

from ...comum.models.base import SoftDeleteModel

class Papel(SoftDeleteModel):
    """
    Representa um conjunto de permissões atribuídas a uma função/cargo.
    Ex: Administrador, Gerente de Operações, Supervisor de Frota
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, default='')
    permissoes = models.ManyToManyField(
        'autenticacao.Permissao',
        blank=True,
        related_name='papeis'
    )

    class Meta:
        db_table = 'papeis'
        verbose_name = 'Papel'
        verbose_name_plural = 'Papéis'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if self.nome:
            self.nome = self.nome.strip()
