from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.contratos.models import ContratoFiliais
from apps.contratos.serializers import (
    ContratoFiliaisSerializer
)
from apps.contratos.services import (
    ContratoFiliaisService
)

class ContratoFiliaisViewSet(viewsets.ModelViewSet):
    queryset = ContratoFiliais.objects.all()
    serializer_class = ContratoFiliaisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subcontrato = ContratoFiliaisService.criar_subcontrato(serializer.validated_data)
        return Response(self.get_serializer(subcontrato).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        subcontrato = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subcontrato = ContratoFiliaisService.atualizar_subcontrato(subcontrato, serializer.validated_data)
        return Response(self.get_serializer(subcontrato).data)