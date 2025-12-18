from typing import List, Any

class ServiceUtils:
    """
    Utilitários para camadas de serviço.
    """

    @staticmethod
    def sincronizar_lista_aninhada(
        entidade_pai: Any,
        dados_lista: List[dict],
        service_filho: Any,
        user: Any,
        metodo_busca_existentes: str,
        metodo_criar: str = 'create',
        campo_entidade_pai: str = 'entidade'
    ) -> None:
        """
        Sincroniza lista aninhada de forma genérica e segura.

        Funcionalidades:
        1. Identifica itens a criar, atualizar e excluir.
        2. Garante a segurança de propriedade usando a lista de existentes (não confia apenas no ID).
        3. Suporta tanto GFK (Anexos) quanto FKs explícitas (Endereços, Contatos).

        Args:
            entidade_pai: A instância do pai (ex: PessoaJuridica).
            dados_lista: A lista de dicts com os dados novos/editados.
            service_filho: A classe de serviço da entidade filha (ex: EnderecoService).
            model_filho: O model da entidade filha (ex: PessoaJuridicaEndereco).
            user: O usuário realizando a ação (para auditoria).
            metodo_busca_existentes: Nome do método no service para listar os itens atuais.
            metodo_criar: Nome do método no service para criar novos itens (default: 'create').
            campo_entidade_pai: Nome do argumento que recebe o pai no método de criação (default: 'entidade').
        """
        
        # 1. Buscar itens existentes (Fonte da Verdade para segurança)
        metodo_busca = getattr(service_filho, metodo_busca_existentes)
        itens_existentes_qs = metodo_busca(entidade_pai)
        
        # Cria um mapa {str(ID): Instancia} para acesso rápido e seguro
        # Isso garante que só mexeremos em objetos que REALMENTE pertencem ao pai
        mapa_existentes = {str(item.pk): item for item in itens_existentes_qs}

        # 2. Identificar IDs recebidos no payload
        ids_recebidos = set()
        for item in dados_lista:
            item_id = item.get('id')
            if item_id:
                ids_recebidos.add(str(item_id))

        # 3. EXCLUIR (Delete)
        # Se está no banco (mapa_existentes) mas não veio na lista (ids_recebidos), exclui.
        for id_existente, item_db in mapa_existentes.items():
            if id_existente not in ids_recebidos:
                service_filho.delete(item_db, user=user)

        # 4. PROCESSAR (Create / Update)
        metodo_create_ref = getattr(service_filho, metodo_criar)

        for item_data in dados_lista:
            item_id = item_data.get('id')

            if item_id:
                # ATUALIZAR (Update)
                # Verifica se o ID existe no mapa de itens que pertencem ao pai.
                # Se não estiver no mapa, ignoramos (segurança contra IDOR - Insecure Direct Object Reference)
                instancia = mapa_existentes.get(str(item_id))
                
                if instancia:
                    service_filho.update(instancia, updated_by=user, **item_data)
            else:
                # CRIAR (Create)
                # Prepara os argumentos dinâmicos para a criação
                item_data.pop('id', None)
                kwargs_criacao = {
                    campo_entidade_pai: entidade_pai,
                    'created_by': user,
                    **item_data
                }
                metodo_create_ref(**kwargs_criacao)