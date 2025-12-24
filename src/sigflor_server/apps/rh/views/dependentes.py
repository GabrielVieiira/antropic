# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.comum.views.base import BaseRBACViewSet
from ..models import Dependente
from ..serializers import DependenteSerializer, DependenteUpdateSerializer
from ..services import DependenteService
from .. import selectors

class DependenteViewSet(BaseRBACViewSet):
    
    permissao_leitura = 'rh_dependentes_ler'
    permissao_escrita = 'rh_dependentes_escrever'
    permissoes_acoes = {
        'incluir_ir': 'rh_dependentes_escrever',
        'excluir_ir': 'rh_dependentes_escrever',
        'incluir_plano_saude': 'rh_dependentes_escrever',
        'excluir_plano_saude': 'rh_dependentes_escrever',
        'estatisticas': 'rh_dependentes_ler',
        'funcionarios_com_dependentes': 'rh_dependentes_ler',
    }

    queryset = Dependente.objects.filter(deleted_at__isnull=True)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return DependenteUpdateSerializer
        return DependenteSerializer

    def perform_update(self, serializer):
        pf_data = serializer.validated_data.pop('pessoa_fisica', None)
        
        DependenteService.update(
            dependente=serializer.instance,
            updated_by=self.request.user,
            pessoa_fisica_data=pf_data,
            **serializer.validated_data
        )

    def perform_destroy(self, instance):
        DependenteService.delete(instance, user=self.request.user)

    @action(detail=True, methods=['post'])
    def incluir_ir(self, request, pk=None):
        dependente = self.get_object()
        DependenteService.atualizar_dependencia_irrf(
            dependente, dependencia_irrf=True, updated_by=request.user
        )
        return Response(self.get_serializer(dependente).data)

    @action(detail=True, methods=['post'])
    def excluir_ir(self, request, pk=None):
        dependente = self.get_object()
        DependenteService.atualizar_dependencia_irrf(
            dependente, dependencia_irrf=False, updated_by=request.user
        )
        return Response(self.get_serializer(dependente).data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        stats = selectors.estatisticas_dependentes(user=request.user)
        return Response(stats)

