from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EnderecoViewSet

enderecos_routers = DefaultRouter()
enderecos_routers.register('', EnderecoViewSet)

urlpatterns = [
    path('enderecos/',include(enderecos_routers.urls)),
]