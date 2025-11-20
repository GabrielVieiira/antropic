from django.db.models import Prefetch

from .models import Endereco

class EnderecosSelector:
    @staticmethod
    def buscar_enderecos():
        enderecos = Prefetch(
            'enderecos', queryset=Endereco.objects.filter(deleted_at__isnull=True).order_by('-principal')
            )
        return enderecos