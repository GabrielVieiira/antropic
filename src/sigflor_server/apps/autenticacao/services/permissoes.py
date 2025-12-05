from typing import Optional
from django.db import transaction

from ..models import Permissao


class PermissaoService:
    """Service layer para operações com Permissão."""

    @staticmethod
    @transaction.atomic
    def create(
        codigo: str,
        nome: str,
        descricao: Optional[str] = None,
        created_by=None,
    ) -> Permissao:
        """Cria uma nova Permissão."""
        permissao = Permissao(
            codigo=codigo,
            nome=nome,
            descricao=descricao,
            created_by=created_by,
        )
        permissao.save()
        return permissao

    @staticmethod
    @transaction.atomic
    def update(permissao: Permissao, updated_by=None, **kwargs) -> Permissao:
        """Atualiza uma Permissão existente."""
        for attr, value in kwargs.items():
            if hasattr(permissao, attr):
                setattr(permissao, attr, value)
        permissao.updated_by = updated_by
        permissao.save()
        return permissao

    @staticmethod
    @transaction.atomic
    def delete(permissao: Permissao, user=None) -> None:
        """Soft delete de uma Permissão."""
        permissao.delete(user=user)

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Permissao]:
        """Busca Permissão por código."""
        return Permissao.objects.filter(
            codigo=codigo,
            deleted_at__isnull=True
        ).first()



