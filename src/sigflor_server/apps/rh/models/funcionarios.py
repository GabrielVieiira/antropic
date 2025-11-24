from django.db import models
from apps.comum.models.base import SoftDeleteModel

class Funcionario(SoftDeleteModel):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
    ]
    ESCOLARIDADE_CHOICES = [
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('superior', 'Ensino Superior'),
        ('pos_graduacao', 'Pós-graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]
    RACA_CORES_CHOICES = [
        ('branca', 'Branca'),
        ('preta', 'Preta'),
        ('parda', 'Parda'),
        ('amarela', 'Amarela'),
        ('indigena', 'Indígena'),
    ]

    nome = models.CharField(
        max_length=200,
        help_text="Nome do funcionário"
    )
    dt_nascimento = models.DateField(
        help_text="Data de nascimento do funcionário"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        help_text="Sexo do funcionário"
    )
    estado_civil = models.CharField(
        max_length=20,
        choices=ESTADO_CIVIL_CHOICES,
        help_text="Estado civil do funcionário"
    )
    escolaridade = models.CharField(
        max_length=20,
        choices=ESCOLARIDADE_CHOICES,
        help_text="Nível de escolaridade do funcionário"
    )
    raca_cor = models.CharField(
        max_length=20,
        choices=RACA_CORES_CHOICES,
        help_text="Raça/Cor do funcionário"
    )
    possui_deficiencia = models.BooleanField(
        default=False,
        help_text="Indica se o funcionário possui alguma deficiência"
    )
    possui_dependentes = models.BooleanField(
        default=False,
        help_text="Indica se o funcionário possui dependentes"
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