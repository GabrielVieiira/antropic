from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.comum.permissions import HasPermission

class BaseRBACViewSet(viewsets.ModelViewSet):
    """
    ViewSet base com suporte a RBAC padrão e ações customizadas.
    
    Atributos:
        permissao_leitura (str): Código para list/retrieve.
        permissao_escrita (str): Código para create/update/destroy.
        permissoes_acoes (dict): Mapeamento { 'nome_da_action': 'codigo_permissao' }.
    """
    permissao_leitura = None
    permissao_escrita = None
    permissoes_acoes = None

    def get_permissions(self):

        permissao_classes = [IsAuthenticated]

        if self.permissoes_acoes and self.action in self.permissoes_acoes:
            permissoes_requeridas = self.permissoes_acoes.get(self.action)
        
        elif self.action in ['list', 'retrieve']:
            permissoes_requeridas = self.permissao_leitura
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissoes_requeridas = self.permissao_escrita
        else:
            permissoes_requeridas = None

        if permissoes_requeridas:
            permissao_classes.append(HasPermission(permissoes_requeridas))
            
        return [permission() for permission in permissao_classes]