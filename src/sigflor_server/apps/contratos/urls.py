from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.contratos.views import (
    ContratoContratanteViewSet,
    ContratoFiliaisViewSet
)

router = DefaultRouter()
router.register(r'contratos', ContratoContratanteViewSet, basename='contrato-contratante')
router.register(r'subcontratos', ContratoFiliaisViewSet, basename='contrato-filial')

urlpatterns = [
    path('', include(router.urls)),
]