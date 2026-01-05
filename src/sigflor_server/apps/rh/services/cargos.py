# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.autenticacao.models import Usuario
from apps.comum.services.utils import ServiceUtils
from .cargo_documento import CargoDocumentoService
from ..models import Cargo


class CargoService:
    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: Usuario,
        nome: str,
        nivel: str,
        documentos: list = None,
        **kwargs
    ) -> Cargo:

        cargo = Cargo(
            nome=nome,
            nivel=nivel,
            created_by=user,
            **kwargs
        )
        cargo.save()

        if documentos:
            for doc_data in documentos:
                CargoDocumentoService.configurar_documento_para_cargo(
                    cargo=cargo,
                    created_by=user,
                    **doc_data
                )

        return cargo

    @staticmethod
    @transaction.atomic
    def update(cargo: Cargo, user: Usuario, **kwargs) -> Cargo:
        documentos = kwargs.pop('documentos', None)
        for attr, value in kwargs.items():
            if hasattr(cargo, attr):
                setattr(cargo, attr, value)
        cargo.updated_by = user
        cargo.save()
        if documentos is not None:           
            ServiceUtils.sincronizar_lista_aninhada(
                entidade_pai=cargo,
                dados_lista=documentos,
                service_filho=CargoDocumentoService,
                user=user,
                metodo_busca_existentes='get_todos_documentos_para_cargo',
                metodo_criar='configurar_documento_para_cargo',
                campo_entidade_pai='cargo'
            )
        return cargo

    @staticmethod
    @transaction.atomic
    def delete(cargo: Cargo, user: Usuario) -> None:
        if cargo.funcionarios.filter(deleted_at__isnull=True).exists():
            raise ValidationError(
                'Não é possível excluir um cargo com funcionários vinculados.'
            )
        cargo.delete(user=user)

    @staticmethod
    @transaction.atomic
    def ativar(cargo: Cargo, updated_by:Usuario) -> Cargo:
        cargo.ativo = True
        cargo.updated_by = updated_by
        cargo.save()
        return cargo

    @staticmethod
    @transaction.atomic
    def desativar(cargo: Cargo, updated_by:Usuario) -> Cargo:
        cargo.ativo = False
        cargo.updated_by = updated_by
        cargo.save()
        return cargo

