from typing import Dict, Any, Optional
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError as DjangoVE
from rest_framework.exceptions import ValidationError as DRFVE

from apps.empresas.models import EmpresaCNPJ
from apps.contatos.service import ContatoService
from apps.contatos.models import Contato
from apps.enderecos.service import EnderecoService
from apps.enderecos.models import Endereco

class EmpresaCNPJService:
    @staticmethod
    @transaction.atomic
    def create_empresa(data: Dict[str, Any] , user=None) -> Dict[str, Any]:
        enderecos_data:list[Optional[dict]]    = data.pop('enderecos', []) or []
        contatos_data:list[Optional[dict]]     = data.pop('contatos', []) or []
        uid = user.pk if getattr(user, 'is_authenticated', False) else None
        try:
            nova_empresa:EmpresaCNPJ    = EmpresaCNPJ(created_by_id=uid, **data)
            nova_empresa.save()           
            enderecos:list[Endereco]    = EnderecoService.criar_enderecos_vinculados(enderecos_data, nova_empresa, uid) if enderecos_data else []
            contatos:list[Contato]      = ContatoService.criar_contatos_vinculados(contatos_data, nova_empresa, uid) if contatos_data else []

            return EmpresaCNPJService._montar_read_model(nova_empresa, enderecos, contatos)
        
        #mapear todos os erros possíveis de empresaCNPJ para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    @staticmethod
    @transaction.atomic
    def update_empresa(empresa: EmpresaCNPJ, data: Dict[str, Any], user, replace:bool) -> EmpresaCNPJ:
        enderecos_data:list[Optional[dict]]    = data.pop('enderecos', []) or []
        contatos_data:list[Optional[dict]]     = data.pop('contatos', []) or []
        uid = user.pk if getattr(user, 'is_authenticated', False) else None

        try:
            for k, v in data.items():
                setattr(empresa, k, v)
            empresa.updated_by = uid
            empresa.save()

            enderecos = EnderecoService.atualizar_enderecos_vinculados(empresa, user, enderecos_data, replace) if enderecos_data else []            
            contatos = ContatoService.atualizar_contatos_vinculados(empresa, user, contatos_data, replace) if contatos_data else []

            return empresa
        
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    @staticmethod
    def _montar_read_model(entidade:EmpresaCNPJ, enderecos:list[Optional[Endereco]], contatos:list[Optional[Contato]]) -> Dict[str, Any]:
        enderecos_out = [
            {
                'id': e.pk,
                'logradouro': e.logradouro,
                'numero': e.numero or '',
                'complemento': e.complemento,
                'bairro': e.bairro or '',
                'cidade': e.cidade,
                'estado': e.estado,
                'cep': e.cep,
                'pais': e.pais,
                'principal': e.principal,
                'deleted_at': e.deleted_at,
                'created_at': e.created_at,
                'updated_at': e.updated_at,
            } for e in enderecos] if enderecos else []

        contatos_out = [
            {
                'id': c.pk,
                'tipo': c.tipo,
                'valor': c.valor,
                'principal': c.principal,
                'deleted_at': c.deleted_at,
                'created_at': c.created_at,
                'updated_at': c.updated_at,
            } for c in contatos] if contatos else []

        return {
            'id': entidade.pk,
            'razao_social': entidade.razao_social,
            'cnpj': entidade.cnpj,
            'cnpj_formatado': entidade.cnpj_formatado,
            'deleted_at': entidade.deleted_at,
            'created_at': entidade.created_at,
            'updated_at': entidade.updated_at,
            'enderecos': enderecos_out,
            'contatos': contatos_out,
        }

    @staticmethod
    @transaction.atomic
    def soft_delete_empresa(empresa: EmpresaCNPJ, user):
        empresa.ativo = False
        empresa.updated_by = user
        empresa.save(update_fields=['ativo', 'updated_by', 'updated_at'])
        # Preciso implementar a remoção lógica de endereços e contatos vinculados!
