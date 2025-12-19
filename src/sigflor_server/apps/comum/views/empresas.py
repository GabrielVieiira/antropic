from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .base import BaseRBACViewSet
from ..models import Empresa
from ..serializers import (
    EmpresaSerializer, 
    EmpresaCreateSerializer, 
    EmpresaListSerializer
)
from ..services import EmpresaService
from .. import selectors


class EmpresaViewSet(BaseRBACViewSet):
    
    permissao_leitura = 'comum_empresas_ler'
    permissao_escrita = 'comum_empresas_escrever'
    permissoes_acoes =  {
        'tornar_matriz': 'comum_empresas_escrever',
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return EmpresaCreateSerializer
        return EmpresaSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        ativa = self.request.query_params.get('ativa')

        if ativa is not None:
            ativa = ativa.lower() == 'true'

        return selectors.empresa_list(search=search, ativa=ativa)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pessoa_juridica_data = serializer.validated_data.pop('pessoa_juridica')
        descricao = serializer.validated_data.get('descricao', '')
        ativa = serializer.validated_data.get('ativa', True)
        empresa = EmpresaService.create(
            user=request.user, 
            pessoa_juridica_data=pessoa_juridica_data,
            descricao=descricao,
            ativa=ativa
        )
        output_serializer = EmpresaSerializer(empresa)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        pj_data = serializer.validated_data.pop('pessoa_juridica', None)
        
        EmpresaService.update(
            empresa=serializer.instance,
            updated_by=self.request.user,
            pessoa_juridica=pj_data,
            **serializer.validated_data
        )

    def retrieve(self, request, pk=None):
        empresa = selectors.empresa_detail(pk=pk)
        serializer = self.get_serializer(empresa)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        EmpresaService.delete(instance, user=self.request.user)

    @action(detail=True, methods=['post'])
    def tornar_matriz(self, request, pk=None):
        empresa = self.get_object()
        EmpresaService.tornar_matriz(
            empresa, 
            updated_by=request.user
        )
        serializer = self.get_serializer(empresa)
        return Response(serializer.data)