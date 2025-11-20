from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaCNPJViewSet,
    ContratanteViewSet,
    FilialViewSet,
)

empresas_router = DefaultRouter()
empresas_router.register(r'empresas-cnpj', EmpresaCNPJViewSet, basename='empresas-cnpj')
empresas_router.register(r'contratantes', ContratanteViewSet, basename='contratante')
empresas_router.register(r'filiais', FilialViewSet, basename='filial')

urlpatterns = [
    path('empresas/', include(empresas_router.urls)),
]
