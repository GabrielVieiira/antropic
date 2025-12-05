from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Permissao
from ..serializers import PermissaoSerializer
from ..services import PermissaoService
from .. import selectors


class PermissaoViewSet(viewsets.ModelViewSet):
    """ViewSet para Permissao."""

    queryset = Permissao.objects.filter(deleted_at__isnull=True)
    serializer_class = PermissaoSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        return selectors.permissao_list(search=search)

    def destroy(self, request, pk=None):
        try:
            permissao = Permissao.objects.get(pk=pk, deleted_at__isnull=True)
            PermissaoService.delete_permissao(
                permissao,
                user=request.user if request.user.is_authenticated else None
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Permissao.DoesNotExist:
            return Response(
                {'detail': 'Permissão não encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )