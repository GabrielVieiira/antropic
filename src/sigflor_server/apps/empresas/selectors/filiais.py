from typing import Optional, Dict, Any
from django.db.models import QuerySet

from apps.empresas.models import Filial

class FiliaisSelector:
    @staticmethod
    def base_qs(user=None)-> QuerySet[Filial]:
        """
        Ponto único para aplicar escopos globais:
        - ativos
        - soft delete (se usar)
        - escopo por regional/CNPJ via user (se necessário)
        """
        qs = Filial.objects.all()
        # Exemplo de escopo por usuário/tenant (ajuste conforme sua regra):
        # if user and not user.is_superuser:
        #     qs = qs.filter(minha_regra_de_escopo=...)
        return qs

    @staticmethod
    def list_filiais(filters: Optional[Dict[str, Any]] = None, user=None) -> list[Filial]:
        qs = FiliaisSelector.base_qs(user=user)
        return qs
