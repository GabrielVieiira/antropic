from typing import Optional, Dict, Any
from django.db.models import QuerySet

from apps.empresas.models import Contratante

class ContratantesSelector():
    @staticmethod
    def base_qs(user=None)-> QuerySet[Contratante]:
        """
        Ponto único para aplicar escopos globais:
        - ativos
        - soft delete (se usar)
        - escopo por regional/CNPJ via user (se necessário)
        """
        qs = Contratante.objects.all()
        # Exemplo de escopo por usuário/tenant (ajuste conforme sua regra):
        # if user and not user.is_superuser:
        #     qs = qs.filter(minha_regra_de_escopo=...)
        return qs
    
    @staticmethod
    def list_contratantes(filters: Optional[Dict[str, Any]] = None, user=None) -> list[Contratante]:
        qs = ContratantesSelector.base_qs(user=user)
        return qs
