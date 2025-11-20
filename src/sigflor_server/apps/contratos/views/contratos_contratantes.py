from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.contratos.models import ContratoContratante
from apps.contratos.serializers import (
    ContratoContratanteSerializer
)
from apps.contratos.services import (
    ContratoContratanteService
)


class ContratoContratanteViewSet(viewsets.ModelViewSet):
    queryset = ContratoContratante.objects.all()
    serializer_class = ContratoContratanteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contrato = ContratoContratanteService.criar_contrato_contratante(serializer.validated_data)
        return Response(self.get_serializer(contrato).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        contrato = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contrato = ContratoContratanteService.atualizar_contrato_contratante(contrato, serializer.validated_data)
        return Response(self.get_serializer(contrato).data, status=status.HTTP_200_OK)