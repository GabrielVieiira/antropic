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

    @staticmethod
    def get_deficiencias_pessoa_fisica(pessoa_fisica) -> list:
        return list(Deficiencia.objects.filter(
            pessoa_fisica=pessoa_fisica,
            deleted_at__isnull=True
        ))
    
    @staticmethod
    @transaction.atomic
    def atualizar_deficiencias_pessoa_fisica(
        pessoa_fisica: PessoaFisica,
        lista_deficiencias: list,
        user=None
    ):
        if lista_deficiencias is None:
            return

        ids_recebidos_raw = [str(item['id']) for item in lista_deficiencias if item.get('id')]
        ids_recebidos_set = set(ids_recebidos_raw)

        existentes_list = DeficienciaService.get_deficiencias_pessoa_fisica(pessoa_fisica)
        existentes_map = {str(d.id): d for d in existentes_list}

        for deficiencia_id, deficiencia in existentes_map.items():
            if deficiencia_id not in ids_recebidos_set:
                DeficienciaService.delete(deficiencia, user=user)

        for item in lista_deficiencias:
            item_id = str(item.get('id')) if item.get('id') else None

            if item_id and item_id not in existentes_map:
                raise ValidationError({
                    "deficiencias": [f"A deficiência com id '{item_id}' não foi encontrada ou não pertence a esta pessoa física."]
                })

            if not item_id:
                dados_create = {k:v for k,v in item.items() if k != 'id'}
                DeficienciaService.create(
                    pessoa_fisica=pessoa_fisica,
                    created_by=user,
                    **dados_create
                )
                continue

            deficiencia = existentes_map[item_id]
            DeficienciaService.update(deficiencia, updated_by=user, **item)

        return pessoa_fisica