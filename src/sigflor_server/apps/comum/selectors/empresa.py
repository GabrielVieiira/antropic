from django.db.models import QuerySet, Q
from ..models import Empresa

def empresa_list(*, filters: dict = None, search: str = None, ativa: bool = None) -> QuerySet:
    qs = Empresa.objects.filter(deleted_at__isnull=True).select_related('pessoa_juridica')

    if ativa is not None:
        qs = qs.filter(ativa=ativa)

    if filters:
        qs = qs.filter(**filters)

    if search:
        qs = qs.filter(
            Q(pessoa_juridica__razao_social__icontains=search) |
            Q(pessoa_juridica__cnpj__icontains=search)
        )

    return qs.order_by('pessoa_juridica__razao_social')


def empresa_detail(*, pk) -> Empresa:
    return Empresa.objects.select_related(
        'pessoa_juridica'
    ).prefetch_related(
        'pessoa_juridica__enderecos_vinculados__endereco',
        'pessoa_juridica__contatos_vinculados__contato',
        'pessoa_juridica__documentos_vinculados__documento'
    ).get(pk=pk, deleted_at__isnull=True)
