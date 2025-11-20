from django.db.models import Model
from typing import Dict, Any
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError as DjangoVE
from rest_framework.exceptions import ValidationError as DRFVE
from django.db import IntegrityError, transaction

from .models import Endereco
class EnderecoService:
    @staticmethod
    def criar_enderecos_vinculados(enderecos_data:list[Dict[str,Any]], objeto:Model, uid)-> list[Endereco]:
        try:
            enderecos_criados: list = []
            if enderecos_data and not any(e.get('principal') for e in enderecos_data):
                raise DRFVE({'Endereco':'Defina algum endereço como principal.'})

            objeto_pai_ct:ContentType = ContentType.objects.get_for_model(objeto)
            objeto_pai_id:int         = objeto.pk
            for e in enderecos_data:
                e['content_type'] = objeto_pai_ct
                e['object_id']    = objeto_pai_id
                end = Endereco(created_by_id=uid, **e)
                end.save()
                enderecos_criados.append(end)
            return enderecos_criados

        #mapear todos os erros possíveis de endereços para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    @transaction.atomic
    @staticmethod   
    def atualizar_enderecos_vinculados(objeto:Model, user, enderecos_data:list[Dict[str,Any]], replace:bool) -> None:
        try:
            enderecos_result = []
            objeto_pai_ct:ContentType = ContentType.objects.get_for_model(objeto)
            objeto_pai_id:int         = objeto.pk
            user = user.pk if getattr(user, 'is_authenticated', False) else None

            if replace:
                Endereco.objects.filter(content_type=objeto_pai_ct, object_id=objeto_pai_id).delete(user=user)
                for e in enderecos_data:
                    if e.get('id'):
                        raise DRFVE({'enderecos': 'Não é possível usar ID ao substituir endereços. IDs são usados apenas para atualizações parciais.'})
                    e['content_type'] = objeto_pai_ct
                    e['object_id']    = objeto_pai_id
                    novo_endereco = Endereco(created_by_id=user, **e)
                    novo_endereco.save()
                    enderecos_result.append(novo_endereco)
                return enderecos_result

            if enderecos_data and any(e.get('principal') for e in enderecos_data):
                objeto.enderecos.update(principal=False)

            for e in enderecos_data:
                if e.get('id'):
                    endereco = Endereco.objects.filter(pk=e['id'], content_type=objeto_pai_ct, object_id=objeto_pai_id).first()
                    if not endereco:
                        raise DRFVE({'enderecos': f'Endereço com ID {e["id"]} não encontrado para o objeto especificado.'})
                    for k, v in e.items():
                        setattr(endereco, k, v)
                    endereco.updated_by = user
                    endereco.save()
                else:
                    e['content_type'] = objeto_pai_ct
                    e['object_id']    = objeto_pai_id
                    novo_endereco = Endereco(created_by_id=user, **e)
                    novo_endereco.save()
                    enderecos_result.append(novo_endereco)
            return enderecos_result

        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})

    @staticmethod   
    def remover_enderecos_vinculados():
        try:
            pass
        #mapear todos os erros possíveis de endereços para DRFVE
        except DjangoVE as e:
            if hasattr(e, 'message_dict'):
                raise DRFVE(e.message_dict)
            raise DRFVE({'aviso': e.messages})
        except IntegrityError as e:
            raise DRFVE({'aviso': str(e)})