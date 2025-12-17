import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UsuarioManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('O username é obrigatório')
        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ativo', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True, help_text='Controla acesso ao sistema')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    papeis = models.ManyToManyField(
        'autenticacao.Papel',
        blank=True,
        related_name='usuarios'
    )

    permissoes_diretas = models.ManyToManyField(
        'autenticacao.Permissao',
        blank=True,
        related_name='usuarios_diretos'
    )

    allowed_filiais = models.ManyToManyField(
        'comum.Filial',
        blank=True,
        related_name='usuarios_com_acesso',
        help_text='Filiais às quais o usuário tem permissão para acessar e gerenciar.'
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'

    def delete(self, user=None):
        self.deleted_at = timezone.now()
        self.ativo = False
        self.save(update_fields=['deleted_at', 'ativo', 'updated_at'])

    def restore(self):
        self.deleted_at = None
        self.ativo = True
        self.save(update_fields=['deleted_at', 'ativo', 'updated_at'])

    @property
    def is_active(self):
        return self.ativo and self.deleted_at is None

    def get_permissoes_efetivas(self):
        """
        Retorna todas as permissões efetivas do usuário.
        Combina permissões diretas + permissões dos papéis.
        """
        if self.is_superuser:
            from .permissoes import Permissao
            return Permissao.objects.all()

        permissoes_papeis = set()
        for papel in self.papeis.all():
            permissoes_papeis.update(papel.permissoes.all())

        permissoes_diretas = set(self.permissoes_diretas.all())

        return permissoes_papeis | permissoes_diretas

    def tem_permissao(self, codigo_permissao: str) -> bool:
        if self.is_superuser:
            return True
        return any(p.codigo == codigo_permissao for p in self.get_permissoes_efetivas())
