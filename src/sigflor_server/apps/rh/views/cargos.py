# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.comum.views.base import BaseRBACViewSet
from ..models import Cargo
from ..serializers import (
    CargoSerializer,
    CargoCreateSerializer,
    CargoListSerializer,
    FuncionarioListSerializer
)
from ..services import CargoService
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
        if self.action in ['create', 'update', 'partial_update']:
            return CargoCreateSerializer
        return CargoSerializer

    def get_queryset(self):
        busca = self.request.query_params.get('busca')
        ativo = self.request.query_params.get('ativo')
        cbo = self.request.query_params.get('cbo')
        nivel = self.request.query_params.get('nivel')
        com_risco = self.request.query_params.get('com_risco')

        if ativo is not None:
            ativo = ativo.lower() == 'true'
        if com_risco is not None:
            com_risco = com_risco.lower() == 'true'

        return selectors.cargo_list(
            user=self.request.user,
            busca=busca,
            ativo=ativo,
            cbo=cbo,
            nivel=nivel,
            com_risco=com_risco
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        documentos_exigidos = serializer.validated_data.pop('documentos_exigidos', [])

        cargo = CargoService.create(
            user=request.user,
            documentos_exigidos=documentos_exigidos,
            **serializer.validated_data
        )
        output_serializer = CargoSerializer(cargo)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        CargoService.update(
            user = self.request.user,
            cargo=serializer.instance,
            **serializer.validated_data
        )

    def retrieve(self, request, pk=None):
        cargo = selectors.cargo_detail(user=request.user, pk=pk)
        serializer = self.get_serializer(cargo)
        return Response(serializer.data)

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
    def ativos(self, request):
        cargos = selectors.cargos_ativos(user=request.user)
        serializer = CargoListSerializer(cargos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        stats = selectors.estatisticas_cargos(user=request.user)
        return Response(stats)