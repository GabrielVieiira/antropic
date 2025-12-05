from django.db.models import QuerySet, Q
from ..models import Permissao

def permissao_list(*, search: str = None) -> QuerySet:
    """Lista permissoes."""
    qs = Permissao.objects.filter(deleted_at__isnull=True)

    if search:
        qs = qs.filter(
            Q(codigo__icontains=search) |
            Q(nome__icontains=search)
        )

    return qs.order_by('codigo')


