from rest_framework import viewsets

from .models import Endereco
from .serializer import EnderecoOutSerializer

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoOutSerializer