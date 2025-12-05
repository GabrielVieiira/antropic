from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    PermissaoViewSet,
    PapelViewSet,
)

router = DefaultRouter()

# Usuários e permissões
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'permissoes', PermissaoViewSet, basename='permissao')
router.register(r'papeis', PapelViewSet, basename='papel')

urlpatterns = [
    path('', include(router.urls)),
]