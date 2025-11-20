from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContatoViewSet

contatos_routers = DefaultRouter()
contatos_routers.register('', ContatoViewSet)

urlpatterns = [
    path('contatos/',include(contatos_routers.urls)),
]