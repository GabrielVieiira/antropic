from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


from .base import BaseRBACViewSet
from ..serializers import (
    ClienteSerializer, 
    ClienteCreateSerializer,
    ClienteListSerializer
)
from ..services import ClienteService
from .. import selectors


class ClienteViewSet(BaseRBACViewSet):

    permissao_leitura = 'comum_clientes_ler'
    permissao_escrita = 'comum_clientes_escrever'
    permissoes_acoes =  {
        'ativar': 'comum_clientes_escrever',
        'desativar': 'comum_clientes_escrever',
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ClienteCreateSerializer
        return ClienteSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        ativo = self.request.query_params.get('ativo')

        if ativo is not None:
            ativo = ativo.lower() == 'true'

        return selectors.cliente_list(search=search, ativo=ativo)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cliente = ClienteService.create(
            validated_data=serializer.validated_data,
            user=request.user
        )
        output_serializer = ClienteSerializer(cliente)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        cliente = self.get_object()
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        cliente = self.get_object()
        ClienteService.delete(
            cliente, 
            user=request.user
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
            cliente = self.get_object()
            ClienteService.ativar(
                cliente,
                updated_by=request.user
            )
            serializer = self.get_serializer(cliente)
            return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
            cliente = self.get_object()
            ClienteService.desativar(
                cliente,
                updated_by=request.user
            )
            serializer = self.get_serializer(cliente)
            return Response(serializer.data)
