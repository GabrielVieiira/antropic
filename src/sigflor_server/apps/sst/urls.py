# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExameViewSet

router = DefaultRouter()
router.register(r'exames', ExameViewSet, basename='exame')

urlpatterns = [
    path('', include(router.urls)),
]