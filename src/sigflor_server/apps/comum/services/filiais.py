# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from ..models import Filial
from ..models.enums import StatusFilial
from apps.autenticacao.models.usuarios import Usuario


class FilialService:
    """Service layer para operações com Filial."""

    @staticmethod
    def _check_filial_ownership_access(user: Usuario, filial: Filial):
        """
        Verifica se o usuário tem acesso à filial específica. Superusuários sempre têm acesso.
        """
        if user.is_superuser:
            return True
        if not user.allowed_filiais.filter(id=filial.id).exists():
            raise PermissionDenied(f"Usuário não tem acesso à filial {filial.nome}.")
        return True

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: Usuario,
        validated_data: dict,
    ) -> Filial:
        """Cria uma nova Filial, verificando permissão genérica para criação.
        A verificação de permissão genérica será tratada na camada de View.
        """
        # Nenhuma verificação de filial aqui para criação, pois o usuário pode estar criando uma nova filial.
        # A permissão para criar (comum_filial_editar) será verificada na View.
        enderecos = validated_data.pop('enderecos')
        contatos = validated_data.pop('contatos')
        
        print("Creating Filial with data:", validated_data)

        filial = Filial(
            nome=validated_data.get('nome'),
            codigo_interno=validated_data.get('codigo_interno'),
            empresa=validated_data.get('empresa'),
            status=validated_data.get('status'),
            descricao=validated_data.get('descricao'),
            created_by=user,
        )
        filial.save()

        if enderecos:
            from .enderecos import EnderecoService
            for end_data in enderecos:
                EnderecoService.criar_endereco_filial(
                    filial=filial,
                    **end_data
                )

        if contatos:
            from .contatos import ContatoService
            for contato_data in contatos:
                ContatoService.criar_contato_filial(
                    filial=filial,
                    **contato_data
                )

        return filial

    @staticmethod
    @transaction.atomic
    def update(filial: Filial, user: Usuario, updated_by=None, **kwargs) -> Filial:
        """Atualiza uma Filial existente, verificando permissão regional."""
        FilialService._check_filial_ownership_access(user, filial)

        for attr, value in kwargs.items():
            if hasattr(filial, attr):
                setattr(filial, attr, value)
        filial.updated_by = updated_by
        filial.save()
        return filial

    @staticmethod
    @transaction.atomic
    def delete(filial: Filial, user: Usuario) -> None:
        """Soft delete de uma Filial, verificando permissão regional."""
        FilialService._check_filial_ownership_access(user, filial)
        filial.delete(user=user)

    @staticmethod
    @transaction.atomic
    def ativar(filial: Filial, user: Usuario, updated_by=None) -> Filial:
        """Ativa uma filial, verificando permissão regional."""
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.ATIVA
        filial.updated_by = updated_by
        filial.save()
        return filial

    @staticmethod
    @transaction.atomic
    def desativar(filial: Filial, user: Usuario, updated_by=None) -> Filial:
        """Desativa uma filial, verificando permissão regional."""
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.INATIVA
        filial.updated_by = updated_by
        filial.save()
        return filial

    @staticmethod
    @transaction.atomic
    def suspender(filial: Filial, user: Usuario, updated_by=None) -> Filial:
        """Suspende uma filial, verificando permissão regional."""
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.SUSPENSA
        filial.updated_by = updated_by
        filial.save()
        return filial
