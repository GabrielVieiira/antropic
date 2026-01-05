from django.db import transaction
from rest_framework.exceptions import ValidationError

from ..models import Projeto, StatusProjeto
from apps.autenticacao.models import Usuario

class ProjetoService:

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: Usuario,
        descricao: str,
        filial,
        **kwargs
    ) -> Projeto:
        
        filial_id = getattr(filial, 'id', filial)

        projeto = Projeto(
            descricao=descricao,
            filial_id=filial_id,
            created_by=user,
            **kwargs
        )
        projeto.save()
        return projeto

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: Usuario,
        projeto: Projeto,
        **kwargs
    ) -> Projeto:
        
        if 'filial' in kwargs:
            nova_filial = kwargs.pop('filial')
            projeto.filial_id = getattr(nova_filial, 'id', nova_filial)

        for attr, value in kwargs.items():
            if hasattr(projeto, attr):
                setattr(projeto, attr, value)
        
        projeto.updated_by = user
        projeto.save()
        return projeto

        return projeto

    @staticmethod
    @transaction.atomic
    def delete(*, user: Usuario, projeto: Projeto) -> None:
        # Muda status para cancelado antes de deletar logicamente?
        # Ou apenas marca deleted_at. Vamos manter simples:
        projeto.delete(user=user)

    @staticmethod
    @transaction.atomic
    def alterar_status(
        *, 
        user: Usuario, 
        projeto: Projeto, 
        novo_status: str
    ) -> Projeto:
        if novo_status not in StatusProjeto.values:
            raise ValidationError({'status': f"O status '{novo_status}' não é válido."})

        if projeto.status == StatusProjeto.CONCLUIDO and novo_status == StatusProjeto.CANCELADO:
            raise ValidationError("Não é possível cancelar um projeto já concluído.")

        projeto.status = novo_status
        projeto.updated_by = user
        projeto.save()
        
        return projeto