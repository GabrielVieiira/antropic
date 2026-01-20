from typing import Optional
from django.db.models import QuerySet
from ..models import Exame
from apps.autenticacao.models.usuarios import Usuario


def exame_list(*, user: Usuario, search: str = None) -> QuerySet[Exame]:

    qs = Exame.objects.filter(deleted_at__isnull=True)

    if search:
        qs = qs.filter(nome__icontains=search)

    return qs.order_by('nome')


def exame_detail(*, user: Usuario, pk: str) -> Exame:
    return Exame.objects.get(pk=pk, deleted_at__isnull=True)


def exame_get_by_id_irrestrito(*, user: Usuario, pk: str) -> Optional[Exame]:
    return Exame.objects.filter(pk=pk).first()


def exame_list_selection(*, user: Usuario) -> QuerySet[Exame]:
    return Exame.objects.filter(deleted_at__isnull=True).only('id', 'nome').order_by('nome')