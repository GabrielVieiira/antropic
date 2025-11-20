import random
from typing import Dict, Any, Optional
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError as DjangoVE
from rest_framework.exceptions import ValidationError as DRFVE

from apps.empresas.models import Filial
from apps.contatos.service import ContatoService
from apps.contatos.models import Contato
from apps.enderecos.service import EnderecoService
from apps.enderecos.models import Endereco

class FiliaisService:
    @staticmethod
    @transaction.atomic
    def create_filial(data: Dict[str, Any] , user=None) -> Dict[str, Any]:
        enderecos_data = data.pop('enderecos', [])
        contatos_data  = data.pop('contatos', [])
        uid = user.pk if getattr(user, 'is_authenticated', False) else None
        #Definir regra de negócio para cógido interno das filiais
        cod_interno = random.randint(1, 1000)
        try:
            nova_filial = Filial(created_by_id=uid, codigo_interno=cod_interno, **data)
            nova_filial.save()
            enderecos:list[Endereco]    = EnderecoService.criar_enderecos_vinculados(enderecos_data, nova_filial, uid) if enderecos_data else []
            contatos:list[Contato]      = ContatoService.criar_contatos_vinculados(contatos_data, nova_filial, uid) if contatos_data else []
            return FiliaisService._montar_read_model(nova_filial, enderecos, contatos) 
        #mapear todos os erros possíveis de filiais para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    @staticmethod
    @transaction.atomic
    def update_filial(filial: Filial, data: Dict[str, Any], user, replace:bool) -> Filial:
        enderecos_data = data.pop('enderecos', [])
        contatos_data  = data.pop('contatos', [])
        uid = user.pk if getattr(user, 'is_authenticated', False) else None

        try:
            for k, v in data.items():
                setattr(filial, k, v)
            filial.updated_by = uid
            filial.save()

            enderecos = EnderecoService.atualizar_enderecos_vinculados(filial, user, enderecos_data, replace) if enderecos_data else []            
            contatos = ContatoService.atualizar_contatos_vinculados(filial, user, contatos_data, replace) if contatos_data else []
            return FiliaisService._montar_read_model(filial, enderecos, contatos)
        
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    #Compensa centralizar a read model aqui na camada de selector?
    @staticmethod
    def _montar_read_model(entidade:Filial, enderecos:list[Optional[Endereco]], contatos:list[Optional[Contato]]) -> Dict[str, Any]:
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
            'nome': entidade.nome,
            'codigo_interno': entidade.codigo_interno,
            'status': entidade.status,
            'created_at': entidade.created_at,
            'updated_at': entidade.updated_at,
            'enderecos': enderecos_out,
            'contatos': contatos_out,
        }