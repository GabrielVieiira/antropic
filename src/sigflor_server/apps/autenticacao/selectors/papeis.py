from django.db.models import QuerySet, Q
from ..models import Papel

def papel_list(*, search: str = None) -> QuerySet:
    """Lista papeis com permissoes."""
    qs = Papel.objects.filter(deleted_at__isnull=True).prefetch_related('permissoes')

    if search:
        qs = qs.filter(Q(nome__icontains=search))

    return qs.order_by('nome')


def papel_detail(*, pk) -> Papel:
    """Obtem detalhes de um papel com permissoes."""
    return Papel.objects.prefetch_related('permissoes').get(pk=pk, deleted_at__isnull=True)
