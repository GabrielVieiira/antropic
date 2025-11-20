from django.db.models import Model
from typing import Dict, Any
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError as DjangoVE
from rest_framework.exceptions import ValidationError as DRFVE
from django.db import IntegrityError, transaction

from .models import Contato

class ContatoService:
    @staticmethod
    def criar_contatos_vinculados(contatos_data:list[Dict[str,Any]], objeto:Model, uid)-> list[Contato]:
        try:
            contatos_criados = []
            #verificar se tem um contato principal por tipo de contato
            if contatos_data and not any(c.get('principal') for c in contatos_data):
                raise ValueError({'aviso':'Selecione um contato principal.'})
            
            objeto_pai_ct:ContentType = ContentType.objects.get_for_model(objeto)
            objeto_pai_id:int         = objeto.pk
            for c in contatos_data:
                c['content_type'] = objeto_pai_ct
                c['object_id']    = objeto_pai_id
                contato = Contato(created_by_id=uid, **c)
                contato.save()
                contatos_criados.append(contato)
            return contatos_criados
        
        #mapear todos os erros possíveis de contatos para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})
        
    @transaction.atomic
    @staticmethod
    def atualizar_contatos_vinculados(objeto:Model, user, contatos_data:list[Dict[str,Any]], replace:bool) -> list[Contato]:
        try:
            contatos_result = []
            objeto_pai_ct:ContentType = ContentType.objects.get_for_model(objeto)
            objeto_pai_id:int         = objeto.pk
            user = user.pk if getattr(user, 'is_authenticated', False) else None

            if replace:
                Contato.objects.filter(content_type=objeto_pai_ct, object_id=objeto_pai_id).delete(user=user)
                for c in contatos_data:
                    if c.get('id'):
                        raise DRFVE({'contatos': 'Não é possível usar ID ao substituir contatos. IDs são usados apenas para atualizações parciais.'})
                    c['content_type'] = objeto_pai_ct
                    c['object_id']    = objeto_pai_id
                    novo_contato = Contato(created_by_id=user, **c)
                    novo_contato.save()
                    contatos_result.append(novo_contato)
                return contatos_result

            if contatos_data and any(e.get('principal') for e in contatos_data):
                objeto.contatos.update(principal=False)

            for c in contatos_data:
                if c.get('id'):
                    contato = Contato.objects.filter(pk=c['id'], content_type=objeto_pai_ct, object_id=objeto_pai_id).first()
                    if not contato:
                        raise DRFVE({'contatos': f'Contato com ID {e["id"]} não encontrado para o objeto especificado.'})
                    for k, v in c.items():
                        setattr(contato, k, v)
                    contato.updated_by = user
                    contato.save()
                else:
                    c['content_type'] = objeto_pai_ct
                    c['object_id']    = objeto_pai_id
                    novo_contato = Contato(created_by_id=user, **c)
                    novo_contato.save()
                    contatos_result.append(novo_contato)
            return contatos_result
        
        #mapear todos os erros possíveis de contatos para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})
    
    @staticmethod
    def remover_contatos_vinculados():
        try:
            pass
        #mapear todos os erros possíveis de contatos para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})