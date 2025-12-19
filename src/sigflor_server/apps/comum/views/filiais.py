# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .base import BaseRBACViewSet
from ..serializers import FilialSerializer, FilialCreateSerializer, FilialListSerializer
from ..services import FilialService
from .. import selectors


class FilialViewSet(BaseRBACViewSet):

    permissao_leitura = 'comum_filiais_ler'
    permissao_escrita = 'comum_filiais_escrever'
    permissoes_acoes =  {
        'ativar': 'comum_filiais_escrever',
        'desativar': 'comum_filiais_escrever',
        'suspender': 'comum_filiais_escrever',
        'ativas': 'comum_filiais_ler',
        'estatisticas': 'comum_filiais_ler',
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return FilialListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return FilialCreateSerializer
        return FilialSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        status_param = self.request.query_params.get('status')
        empresa_id = self.request.query_params.get('empresa_id')

        return selectors.filial_list(
            user=self.request.user,
            search=search,
            status=status_param,
            empresa_id=empresa_id
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enderecos = serializer.validated_data.pop('enderecos')
        contatos = serializer.validated_data.pop('contatos')
        filial_data = serializer.validated_data
        filial = FilialService.create(
            user = request.user,
            enderecos = enderecos,
            contatos = contatos,
            nome = filial_data.get('nome'),
            codigo_interno = filial_data.get('codigo_interno'),
            status = filial_data.get('status'),
            descricao = filial_data.get('descricao'),
            empresa = filial_data.get('empresa')
        )
        output_serializer = FilialSerializer(filial)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):

        FilialService.update(
            filial=serializer.instance,
            user=self.request.user,
            **serializer.validated_data
        )

    def retrieve(self, request, pk=None):
        filial = selectors.filial_detail(user=request.user,pk=pk)
        serializer = self.get_serializer(filial)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        FilialService.delete(instance, user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        filial = self.get_object()
        FilialService.ativar(
            filial,
            user=request.user
        )
        serializer = self.get_serializer(filial)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        filial = self.get_object()
        FilialService.desativar(
            filial,
            user = request.user
        )
        serializer = self.get_serializer(filial)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def suspender(self, request, pk=None):
        filial = self.get_object()
        FilialService.suspender(
            filial,
            user=request.user
        )
        serializer = self.get_serializer(filial)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ativas(self, request):
        empresa_id = request.query_params.get('empresa_id')
        filiais = selectors.filiais_ativas(
            user=request.user,
            empresa_id=empresa_id
            )
        serializer = FilialListSerializer(filiais, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        stats = selectors.estatisticas_filiais(
            user=request.user
        )
        return Response(stats)
