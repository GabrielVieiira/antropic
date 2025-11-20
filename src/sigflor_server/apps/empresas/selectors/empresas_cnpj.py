from typing import Optional, Dict, Any
from django.db.models import Q, QuerySet

from apps.empresas.models import EmpresaCNPJ
from apps.enderecos.selector import EnderecosSelector
from apps.contatos.selector import ContatosSelector 


class EmpresasCNPJSelector:
    @staticmethod
    def base_qs(user=None)-> QuerySet[EmpresaCNPJ]:
        """
        Ponto único para aplicar escopos globais:
        - ativos
        - soft delete (se usar)
        - escopo por regional/CNPJ via user (se necessário)
        """
        qs = EmpresaCNPJ.objects.all()

        enderecos_vinculados = EnderecosSelector.buscar_enderecos()
        contatos_vinculados = ContatosSelector.buscar_contatos()


        qs = qs.prefetch_related(enderecos_vinculados, contatos_vinculados)
        # Exemplo de escopo por usuário/tenant (ajuste conforme sua regra):
        # if user and not user.is_superuser:
        #     qs = qs.filter(minha_regra_de_escopo=...)
        return qs
    
    @staticmethod
    def list_empresas(filters: Optional[Dict[str, Any]] = None, user=None) -> list[EmpresaCNPJ]:
        """
        Lista paginável/filtrável, já prefetchando endereços e contatos ativos.
        Retorna uma lista de dicts prontos para serialização.
        """
        qs = EmpresasCNPJSelector.base_qs(user=user)

        if filters:
            if s := filters.get("search"):
                qs = qs.filter(Q(razao_social__icontains=s) | Q(cnpj__icontains=s))
            if cnpj := filters.get("cnpj"):
                qs = qs.filter(cnpj=cnpj)
            if not filters.get("incluir_inativos"):
                qs = qs.filter(ativo=True)

        qs = qs.order_by('id')

        return qs