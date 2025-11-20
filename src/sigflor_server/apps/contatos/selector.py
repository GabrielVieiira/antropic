from django.db.models import Prefetch

from .models import Contato

class ContatosSelector:
    @staticmethod
    def buscar_contatos():
        contatos =  Prefetch(
            'contatos', queryset=Contato.objects.filter(deleted_at__isnull=True).order_by('-principal', 'tipo')
            )
        
        return contatos