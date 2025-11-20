from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from apps.empresas.serializers import (
    ContratanteInSerializer,
    ContratanteOutSerializer
)
from apps.empresas.services import ContratanteService
from apps.empresas.selectors import ContratantesSelector

class ContratanteViewSet(viewsets.ModelViewSet):

    serializer_action_classes = {
        "create": ContratanteInSerializer,
        "update": ContratanteInSerializer,
        "partial_update": ContratanteInSerializer,
        "list": ContratanteOutSerializer,
        "retrieve": ContratanteOutSerializer,
    }

    def get_serializer_class(self)-> type[serializers.Serializer]:
        return self.serializer_action_classes.get(self.action, ContratanteOutSerializer)

    def get_queryset(self):
        data = ContratantesSelector.list_contratantes()
        return data

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        input_serializado = serializer_class(data=request.data)
        input_serializado.is_valid(raise_exception=True)
        contratante = ContratanteService.create_contratante(input_serializado.validated_data, request.user)
        output_serializado = ContratanteOutSerializer(contratante)
        return Response(output_serializado.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        objeto = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=objeto, data=request.data)
        serializer.is_valid(raise_exception=True)
        empresa = ContratanteService.update_contratante(objeto, serializer.validated_data, user=request.user, replace=True)
        out_serializer = ContratanteOutSerializer(instance=empresa)
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
        empresa = ContratanteService.update_contratante(objeto, serializer.validated_data, user=request.user, replace=False)
        out_serializer = ContratanteOutSerializer(empresa)
        return Response(out_serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)