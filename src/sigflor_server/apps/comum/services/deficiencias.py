# -*- coding: utf-8 -*-
from typing import Optional
from django.db import transaction

from ..models import Deficiencia, PessoaFisica
from ..models.enums import TipoDeficiencia


class DeficienciaService:

    @staticmethod
    @transaction.atomic
    def create(
        pessoa_fisica: PessoaFisica,
        nome: str,
        tipo: str = '',
        cid: Optional[str] = None,
        grau: Optional[str] = None,
        congenita: bool = False,
        observacoes: Optional[str] = None,
        created_by=None,
    ) -> Deficiencia:
        deficiencia = Deficiencia(
            pessoa_fisica=pessoa_fisica,
            nome=nome,
            tipo=tipo or TipoDeficiencia.OUTRA,
            cid=cid,
            grau=grau,
            congenita=congenita,
            observacoes=observacoes,
            created_by=created_by,
        )
        deficiencia.save()
        return deficiencia

    @staticmethod
    @transaction.atomic
    def update(deficiencia: Deficiencia, updated_by=None, **kwargs) -> Deficiencia:
        kwargs.pop('pessoa_fisica', None)
        kwargs.pop('pessoa_fisica_id', None)
        
        kwargs.pop('data_diagnostico', None)

        for attr, value in kwargs.items():
            if hasattr(deficiencia, attr):
                setattr(deficiencia, attr, value)
        
        deficiencia.updated_by = updated_by
        deficiencia.save()
        return deficiencia

    @staticmethod
    @transaction.atomic
    def delete(deficiencia: Deficiencia, user=None) -> None:
        deficiencia.delete(user=user)
