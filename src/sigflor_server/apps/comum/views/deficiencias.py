from rest_framework.decorators import action
from rest_framework.response import Response
from .base import BaseRBACViewSet
from .. import selectors
from ..serializers import PessoaFisicaSerializer


class DeficienciaRelatoriosViewSet(BaseRBACViewSet): 
    
    permissao_leitura = ''
    permissao_escrita = ''
    permissoes_acoes =  {
        'estatisticas':'comum_deficiencia_ler',
        'pessoas':'comum_deficiencia_ler',
    }

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        stats = selectors.estatisticas_deficiencias()
        return Response(stats)

    @action(detail=False, methods=['get'])
    def pessoas(self, request):
        pessoas = selectors.pessoas_com_deficiencia()
        serializer = PessoaFisicaSerializer(pessoas, many=True)
        return Response(serializer.data)