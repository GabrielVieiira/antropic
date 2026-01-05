import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.comum.views.base import BaseRBACViewSet
from ..models import Cargo
from ..serializers.cargos import (
    CargoSerializer, 
    CargoListSerializer, 
    CargoCreateSerializer, 
    CargoUpdateSerializer,
    CargoSelecaoSerializer
)
from ..serializers.funcionarios import FuncionarioListSerializer
from ..services.cargos import CargoService
from .. import selectors


class CargoViewSet(BaseRBACViewSet):
    
    permissao_leitura = 'rh_cargos_ler'
    permissao_escrita = 'rh_cargos_escrever'
    permissoes_acoes =  {
        'ativar': 'rh_cargos_escrever',
        'desativar': 'rh_cargos_escrever',
        'funcionarios': 'rh_cargos_ler',
        'ativos': 'rh_cargos_ler',
        'estatisticas': 'rh_cargos_ler',
    }

    queryset = Cargo.objects.filter(deleted_at__isnull=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return CargoListSerializer
        if self.action == 'create':
            return CargoCreateSerializer
        if self.action in ['update', 'partial_update']:
            return CargoUpdateSerializer
        if self.action == 'selecao':
            return CargoSelecaoSerializer
        return CargoSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        cbo = self.request.query_params.get('cbo')
        ativo = self.request.query_params.get('ativo')

        if ativo is not None:
            ativo = ativo.lower() == 'true'

        if self.action == 'selecao':
            return selectors.cargo_list_selection()
            
        return selectors.cargo_list(search=search, cbo=cbo, ativo=ativo)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cargo = CargoService.create(
            user=request.user,
            **serializer.validated_data
        )
        return Response(CargoSerializer(cargo).data, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        CargoService.update(
            user = self.request.user,
            cargo=serializer.instance,
            **serializer.validated_data
        )

    def retrieve(self, request, pk=None):
        cargo = selectors.cargo_detail(user = request.user, pk=pk)
        serializer = self.get_serializer(cargo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        CargoService.delete(instance, user=self.request.user)

    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        cargo = self.get_object()
        CargoService.ativar(cargo, updated_by=request.user)
        serializer = self.get_serializer(cargo)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        cargo = self.get_object()
        CargoService.desativar(cargo, updated_by=request.user)
        serializer = self.get_serializer(cargo)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def funcionarios(self, request, pk=None):
        self.get_object() 
        funcionarios = selectors.funcionarios_por_cargo(user=request.user, cargo_id=pk)
        serializer = FuncionarioListSerializer(funcionarios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def selecao(self, request):
        cargos = selectors.cargo_list_selection()
        return Response(self.get_serializer(cargos, many=True).data)