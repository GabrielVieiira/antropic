from django.db.models import QuerySet, Q, Count
from typing import Optional

from ..models import Cargo, Funcionario, RiscoPadrao
from apps.autenticacao.models.usuarios import Usuario

def cargo_list(
    *,
    search: Optional[str],
    cbo: Optional[str],
    ativo: Optional[bool]
) -> QuerySet:
    
    qs = Cargo.objects.filter(deleted_at__isnull=True).prefetch_related(
        'documentos_obrigatorios__documento'
    )

    if cbo:
        qs = qs.filter(cbo=cbo)

    if search:
        qs = qs.filter(
            Q(nome__icontains=search) |
            Q(cbo__icontains=search)
        )

    if ativo is not None:
        qs = qs.filter(ativo=ativo)

    return qs.order_by('nome')

def cargo_detail(*, user:Usuario, pk) -> Cargo:
    return Cargo.objects.prefetch_related(
        'documentos_obrigatorios__documento'
    ).get(pk=pk, deleted_at__isnull=True)

def cargo_list_selection() -> QuerySet:
    return Cargo.objects.filter(
        deleted_at__isnull=True
    ).only('id', 'nome', 'cbo').order_by('nome')

def funcionarios_por_cargo(*, user: Usuario, cargo_id: str) -> QuerySet:
    qs = Funcionario.objects.filter(
        cargo_id=cargo_id,
        deleted_at__isnull=True
    ).select_related('pessoa_fisica', 'projeto')

    if not user.is_superuser:
        qs = qs.filter(
            Q(projeto__filial__in=user.allowed_filiais.all()) |
            Q(projeto__isnull=True)
        ).distinct()

    return qs.order_by('pessoa_fisica__nome_completo')