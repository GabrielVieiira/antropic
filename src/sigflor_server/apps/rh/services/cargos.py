# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.comum.services.utils import ServiceUtils
from ..models import Cargo


class CargoService:

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: Usuario,
        nome: str,
        nivel: str,
        documentos_exigidos: list = None, 
        **dados_cargo
    ) -> Cargo:

        cargo = Cargo(
            nome=nome,
            nivel=nivel,
            created_by=user,
            **dados_cargo
        )
        cargo.save()

        if documentos_exigidos:
            from .cargo_documento import CargoDocumentoService
            
            for doc_data in documentos_exigidos:
                CargoDocumentoService.configurar_documento_para_cargo(
                    cargo=cargo,
                    documento_tipo=doc_data['documento_tipo'],
                    obrigatorio=doc_data.get('obrigatorio', True),
                    condicional=doc_data.get('condicional'),
                    created_by=user
                )

        return cargo

    @staticmethod
    @transaction.atomic
    def update(user: Usuario, cargo: Cargo, **kwargs) -> Cargo:

        documentos_exigidos = kwargs.pop('documentos_exigidos', None)

        for attr, value in kwargs.items():
            if hasattr(cargo, attr):
                setattr(cargo, attr, value)
        
        cargo.updated_by = user
        cargo.save()

        if documentos_exigidos is not None:
            from .cargo_documento import CargoDocumentoService

            ServiceUtils.sincronizar_lista_aninhada(
                entidade_pai=cargo,
                dados_lista=documentos_exigidos,
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
    def ativar(cargo: Cargo, user: Usuario) -> Cargo:
        cargo.ativo = True
        cargo.updated_by = user
        cargo.save()
        return cargo

    @staticmethod
    @transaction.atomic
    def desativar(cargo: Cargo, user: Usuario) -> Cargo:
        cargo.ativo = False
        cargo.updated_by = user
        cargo.save()
        return cargo

