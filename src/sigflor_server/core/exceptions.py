from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError as DjangoValidationError, ObjectDoesNotExist
from django.http import Http404
from django.db.models import ProtectedError

def custom_exception_handler(exc, context):
    """
    Handler global para converter exceções do Django/Service em respostas DRF.
    Padroniza tudo para o formato: { "campo": ["mensagem"], "non_field_errors": ["mensagem"] }
    """
    
    response = exception_handler(exc, context)

    if response is None:
        
        # --- Erros de Validação do Service/Model (400) ---
        if isinstance(exc, DjangoValidationError):
            data = _normalizar_erro_validacao(exc)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # --- Erros de "Não Encontrado" do ORM (404) ---
        if isinstance(exc, ObjectDoesNotExist):
            return Response(
                {'detail': 'Registro não encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # --- Erros de Conflito/Integridade ao Deletar (409) ---
        if isinstance(exc, ProtectedError):
            return Response(
                {
                    'detail': 'Não é possível excluir este item pois ele está vinculado a outros registros.',
                    'vinculos': [str(obj) for obj in exc.protected_objects]
                },
                status=status.HTTP_409_CONFLICT
            )

    return response

def _normalizar_erro_validacao(exc):
    """
    Garante que o erro do Django saia idêntico ao erro de um Serializer do DRF.
    """
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    
    if hasattr(exc, 'messages'):
        return {'non_field_errors': exc.messages}
    
    return {'non_field_errors': [str(exc)]}