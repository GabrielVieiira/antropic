from django.db import models
from apps.comum.models.base import SoftDeleteModel

class Funcionario(SoftDeleteModel):
    
    nome = models.CharField(
        max_length=200,
        help_text="Nome do funcionário"
    )
    dt_nascimento = models.DateField(
        help_text="Data de nascimento do funcionário"
    )

    class Meta:
        db_table = 'funcionarios'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'email'],
                name='uniq_funcionarios_nome_email'
            )
        ]

    def __str__(self):
        return f'{self.nome}'