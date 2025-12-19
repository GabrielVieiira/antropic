# src/sigflor_server/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError, ObjectDoesNotExist

def custom_exception_handler(exc, context):
    """
    Handler global para converter exceções do Django/Service em respostas DRF.
    """
    
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            data = exc.message_dict
        elif hasattr(exc, 'messages'):
            data = {'detail': exc.messages}
        else:
            data = {'detail': str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {'detail': 'Registro não encontrado.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                'detail': 'Verifique os dados informados.',
                'errors': response.data
            }

    return response