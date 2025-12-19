# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from ..models import Filial
from ..models.enums import StatusFilial
from .enderecos import EnderecoService
from .contatos import ContatoService
from .utils import ServiceUtils
from apps.autenticacao.models.usuarios import Usuario


class FilialService:

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
        enderecos : list,
        contatos : list,
        nome: str,
        codigo_interno: str,
        status: str = StatusFilial.ATIVA,
        descricao: str = '',
        empresa=None
    ) -> Filial:

        filial = Filial(
            nome=nome,
            codigo_interno=codigo_interno,
            empresa=empresa,
            status=status,
            descricao=descricao,
            created_by=user,
        )
        filial.save()

        if enderecos:
            from .enderecos import EnderecoService
            for end_data in enderecos:
                EnderecoService.vincular_endereco_filial(
                    filial=filial,
                    **end_data
                )

        if contatos:
            from .contatos import ContatoService
            for contato_data in contatos:
                ContatoService.vincular_contato_filial(
                    filial=filial,
                    **contato_data
                )

        return filial

    @staticmethod
    @transaction.atomic
    def update(filial: Filial, user: Usuario, **kwargs) -> Filial:
        """
        Atualiza uma Filial e sincroniza suas listas aninhadas.
        """

        FilialService._check_filial_ownership_access(user, filial)

        enderecos = kwargs.pop('enderecos', None)
        contatos = kwargs.pop('contatos', None)

        for attr, value in kwargs.items():
            if hasattr(filial, attr):
                setattr(filial, attr, value)
        
        filial.updated_by = user
        filial.save()

        if enderecos is not None:
            ServiceUtils.sincronizar_lista_aninhada(
                entidade_pai=filial,
                dados_lista=enderecos,
                service_filho=EnderecoService,
                user=user,
                metodo_busca_existentes='get_enderecos_filial', #
                metodo_criar='criar_endereco_filial',           #
                campo_entidade_pai='filial'
            )

        if contatos is not None:
            ServiceUtils.sincronizar_lista_aninhada(
                entidade_pai=filial,
                dados_lista=contatos,
                service_filho=ContatoService,
                user=user,
                metodo_busca_existentes='get_contatos_filial', # <--- ATENÇÃO AQUI
                metodo_criar='criar_contato_filial',           #
                campo_entidade_pai='filial'
            )

        return filial

    @staticmethod
    @transaction.atomic
    def delete(filial: Filial, user: Usuario) -> None:
        FilialService._check_filial_ownership_access(user, filial)
        filial.delete(user=user)

    @staticmethod
    @transaction.atomic
    def ativar(filial: Filial, user: Usuario) -> Filial:
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.ATIVA
        filial.updated_by = user
        filial.save()
        return filial

    @staticmethod
    @transaction.atomic
    def desativar(filial: Filial, user: Usuario) -> Filial:
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.INATIVA
        filial.updated_by = user
        filial.save()
        return filial

    @staticmethod
    @transaction.atomic
    def suspender(filial: Filial, user: Usuario) -> Filial:
        FilialService._check_filial_ownership_access(user, filial)
        filial.status = StatusFilial.SUSPENSA
        filial.updated_by = user
        filial.save()
        return filial
