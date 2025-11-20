from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from apps.empresas.serializers import (
    FilialInSerializer, FilialOutSerializer
)
from apps.empresas.services import FiliaisService
from apps.empresas.selectors import FiliaisSelector

class FilialViewSet(viewsets.ModelViewSet):
    
    serializer_action_classes = {
        "create": FilialInSerializer,
        "update": FilialInSerializer,
        "partial_update": FilialInSerializer,
        "list": FilialOutSerializer,
        "retrieve": FilialOutSerializer,
    }

    def get_serializer_class(self)-> type[serializers.Serializer]:
        return self.serializer_action_classes.get(self.action, FilialOutSerializer)
    
    def get_queryset(self):
        data = FiliaisSelector.list_filiais()
        return data

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        input_serializado = serializer_class(data=request.data)
        input_serializado.is_valid(raise_exception=True)
        nova_filial = FiliaisService.create_filial(input_serializado.validated_data, user=request.user)
        out_serializador = FilialOutSerializer(nova_filial)
        return Response(out_serializador.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=objeto, data=request.data)
        serializer.is_valid(raise_exception=True)
        filial = FiliaisService.update_filial(objeto, serializer.validated_data, user=request.user, replace = True)
        out_serializer = FilialOutSerializer(instance=filial)
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
    
    def partial_update(self, request, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=objeto, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        filial = FiliaisService.update_filial(objeto, serializer.validated_data, user=request.user, replace = False)
        out_serializer = FilialOutSerializer(instance=filial)
        return Response(out_serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)