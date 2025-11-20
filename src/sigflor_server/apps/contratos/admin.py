from django.contrib import admin

from .models import ContratoContratante, ContratoFiliais

admin.site.register(ContratoContratante)
admin.site.register(ContratoFiliais)
