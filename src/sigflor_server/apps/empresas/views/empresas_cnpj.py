from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from apps.empresas.serializers import (
    EmpresaCNPJInSerializer, EmpresaCNPJOutSerializer
)
from apps.empresas.services import EmpresaCNPJService
from apps.empresas.selectors import EmpresasCNPJSelector

class EmpresaCNPJViewSet(viewsets.ModelViewSet):

    serializer_action_classes = {
        "create": EmpresaCNPJInSerializer,
        "update": EmpresaCNPJInSerializer,
        "partial_update": EmpresaCNPJInSerializer,
        "list": EmpresaCNPJOutSerializer,
        "retrieve": EmpresaCNPJOutSerializer,
    }

    def get_serializer_class(self) -> type[serializers.Serializer]:
        return self.serializer_action_classes.get(self.action, EmpresaCNPJOutSerializer)

    def get_queryset(self):
        data = EmpresasCNPJSelector.list_empresas()
        return data

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        input_serializado = serializer_class(data=request.data)
        input_serializado.is_valid(raise_exception=True)
        nova_empresa = EmpresaCNPJService.create_empresa(input_serializado.validated_data, user=request.user)
        out_serializer = EmpresaCNPJOutSerializer(nova_empresa)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=objeto, data=request.data)
        serializer.is_valid(raise_exception=True)
        empresa = EmpresaCNPJService.update_empresa(objeto, serializer.validated_data, user=request.user, replace=True)
        out_serializer = EmpresaCNPJOutSerializer(instance=empresa)
        return Response(out_serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs): 
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance = objeto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=objeto, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  
        empresa = EmpresaCNPJService.update_empresa(objeto, serializer.validated_data, user=request.user, replace=False)
        out_serializer = EmpresaCNPJOutSerializer(empresa)
        return Response(out_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)