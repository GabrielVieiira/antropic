from django.contrib import admin

from .models import EmpresaCNPJ, Contratante, Filial

admin.site.register(EmpresaCNPJ)
admin.site.register(Contratante)
admin.site.register(Filial)
