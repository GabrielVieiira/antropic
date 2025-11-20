from rest_framework import viewsets

from .models import Contato
from .serializer import ContatoOutSerializer

class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoOutSerializer