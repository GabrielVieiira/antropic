# Módulo Core — Soft Delete

## 1. Visão Geral

O submódulo **Soft Delete** fornece a infraestrutura central de exclusão lógica do Sigflor.  
Ele garante que registros nunca sejam removidos fisicamente do banco, preservando:

- histórico de dados  
- rastreabilidade  
- integridade referencial  
- auditoria avançada  
- segurança contra exclusões acidentais  

O Soft Delete é aplicado a praticamente todas as entidades do sistema e faz parte do modelo base utilizado pelos demais submódulos do CORE.

---

## 2. Objetivo do Submódulo

- Oferecer um mecanismo padronizado para exclusão lógica  
- Permitir recuperação e consulta de registros excluídos  
- Permitir auditoria precisa (quem excluiu, quando, etc.)  
- Preservar relacionamentos entre entidades  
- Evitar perda de dados históricos  

---

## 3. Arquitetura do Soft Delete

O Soft Delete se baseia em três pilares:

### ✔ 1. Modelo Abstrato (`SoftDeleteModel`)  
Todas as entidades que herdam desse modelo passam a ter suporte automático a:

- `deleted_at`  
- `deleted_by` (opcional, se configurado)  
- lógica de exclusão customizada  

### ✔ 2. QuerySet Customizado (`SoftDeleteQuerySet`)  
Substitui exclusão física por atualização do campo `deleted_at`.

### ✔ 3. Manager Customizado (`SoftDeleteManager`)  
Garante que consultas retornem apenas registros ativos por padrão.

---

## 4. Estrutura Base: Campos e Comportamentos

O `SoftDeleteModel` inclui os seguintes campos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| created_at | datetime | Data de criação |
| updated_at | datetime | Última modificação |
| deleted_at | datetime | Data da exclusão lógica (null = ativo) |
| created_by | FK usuário | Usuário criador (opcional) |
| updated_by | FK usuário | Último editor (opcional) |

O campo mais importante:

### `deleted_at`
- `NULL` → registro ativo  
- `NOT NULL` → registro excluído logicamente  

---

## 5. Métodos Principais

### 5.1 `delete(user=None)`
Substitui exclusão física por:

- registrar usuário que excluiu (se enviado)
- registrar timestamp de exclusão
- evitar violação de integridade referencial
- disparar auditoria avançada

### 5.2 `restore()`
(Disponível quando implementado na service layer)

Reverte a exclusão lógica:

- define `deleted_at = NULL`
- registra em auditoria

### 5.3 `hard_delete()`
Pode ser habilitado apenas para fins administrativos:

- remove o registro fisicamente  
- usado em rotinas internas de limpeza, não exposto ao usuário  

---

## 6. QuerySets e Managers

O Soft Delete utiliza um Manager personalizado:

### `objects`  
Somente registros ativos (`deleted_at IS NULL`)

### `all_objects`  
Retorna todos (ativos + excluídos)

### `deleted_objects`  
Retorna apenas os excluídos (`deleted_at IS NOT NULL`)

---

## 7. Regras de Negócio

1. **Nenhum registro é excluído fisicamente**, salvo via rotinas internas.  
2. Exclusão sempre deve passar por:
   - set de `deleted_at`  
   - atualização de `deleted_by` (quando aplicável)  
   - auditoria avançada  
3. Relações com registros soft-deleted permanecem válidas.  
4. Registros excluídos não aparecem em listagens normais.  
5. Busca explícita pode incluir excluídos apenas via `all_objects`.  
6. Endpoints de exclusão **não removem fisicamente** — apenas acionam soft delete.

---

## 8. Fluxos de Negócio

### 8.1 Exclusão lógica

**Fluxo:**

1. Usuário solicita exclusão de registro.  
2. Service layer chama `instance.delete(user)`.  
3. O modelo:
   - define `deleted_at`  
   - registra `deleted_by` (se disponível)  
   - dispara auditoria avançada  
4. O registro some das listagens normais.  

---

### 8.2 Restauração

1. Apenas usuários administrativos podem restaurar.  
2. A service layer precisa ter um método explícito:  
`instance.restore()`
3. Auditoria registra a ação.  
4. Registros restaurados voltam às listagens normais.

---

### 8.3 Exclusão física (apenas para manutenção interna)

Nunca exposta via API.  
Acontece apenas em:

- rotinas internas de limpeza  
- cenários regulamentares específicos  

---

## 9. Endpoints (API)

O Soft Delete **não possui endpoints próprios**.  
Ele é aplicado automaticamente nos endpoints de exclusão de todos os submódulos.

Exemplo:

### DELETE `/api/core/pessoa-fisica/{id}/`

Comportamento:

- NUNCA remove fisicamente  
- Apenas marca `deleted_at`  
- Retorna `204 No Content`

Exemplo de resposta:

```json
{
"status": "success",
"message": "Registro excluído com sucesso."
}
```

## 10. Erros e Exceções
Código	Mensagem	            Motivo
403	    Sem permissão	        Usuário não pode excluir
404	    Registro não encontrado	Registro não existe ou já está excluído
409	    Não é possível excluir	Regras específicas do módulo

## 11. Observações Técnicas
-  Deve ser herdado por TODAS as entidades que precisam de exclusão lógica.
-  Impacta diretamente o comportamento dos managers e querysets.
-  Evita perda de dados e permite histórico completo.
-  Auditoria avançada deve registrar toda exclusão e restauração.
-  A service layer deve abstrair a lógica de restauração, se utilizada.
-  Recomendado indexar o campo deleted_at para melhorar consultas.
-  Usar all_objects apenas em seletores (selectors) específicos.