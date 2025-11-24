# Módulo Core — Permissões (RBAC)

## 1. Visão Geral

O submódulo **Permissões (RBAC)** é responsável por definir, controlar e aplicar regras de acesso no ERP Sigflor.  
RBAC (*Role-Based Access Control*) permite que as permissões sejam atribuídas com base em papéis (cargos, funções) e não diretamente usuário por usuário.

Dessa forma, o sistema torna-se:

- mais seguro  
- mais organizado  
- mais fácil de administrar  
- mais padronizado entre departamentos  

---

## 2. Objetivo do Submódulo

- Controlar acesso a módulos, ações e rotas  
- Atribuir permissões a papéis (roles)  
- Atribuir papéis a usuários  
- Permitir permissões adicionais específicas  
- Integrar com a camada de autenticação JWT  
- Interagir com logs e auditoria avançada  

O RBAC controla todas as operações:

- leitura  
- criação  
- edição  
- exclusão  
- aprovações  
- acesso às telas e menus  

---

## 3. Componentes do RBAC

O sistema é composto por três entidades principais:

### ✔ 1. **Permissão**  
Unidade mínima de autorização.

### ✔ 2. **Papel (Role)**  
Coleção de permissões por função/cargo.

### ✔ 3. **Usuário**  
Recebe permissões através de papéis e/ou permissões diretas.

---

## 4. Entidade: Permissão

Representa o direito de executar uma ação específica no sistema.

### 4.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador |
| codigo | string | Sim, único | Ex.: `core.pessoa_fisica.listar` |
| nome | string | Sim | Nome amigável |
| descricao | text | Não | Explicação |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |

---

### 4.2 Formato recomendado do campo `codigo`

Um padrão unificado deve ser seguido:
<modulo>.<entidade>.<ação>

Exemplos:
core.usuarios.criar
core.usuarios.listar
core.pessoa_fisica.visualizar
compras.solicitacao.aprovar
frota.veiculo.editar
financeiro.contas_pagar.pagar


---

## 5. Entidade: Papel (Role)

Um papel representa um conjunto de permissões atribuídas a uma função.

### 5.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador |
| nome | string | Sim, único | Ex.: "Supervisor de Frota" |
| descricao | text | Não | Explicação |
| permissoes | ManyToMany → Permissão | Sim | Permissões agrupadas |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |

---

### 5.2 Exemplos de papéis sugeridos

| Papel | Descrição |
|-------|-----------|
| Administrador | Acesso total |
| Gerente de Operações | Acesso às rotinas de campo |
| Supervisor de Frota | Controle de veículos e manutenções |
| RH Administrativo | Gestão de funcionários |
| Financeiro | Contas a pagar e integrações |
| Compras | Solicitações e ordens de compra |

---

## 6. Entidade: Usuário (no contexto RBAC)

O Usuário:

- recebe um ou mais papéis  
- pode receber permissões adicionais  
- pode ter permissões negadas (opcional por regra de negócio)

### 6.1 Relação

Usuario → Papéis (N:N)
Papel → Permissões (N:N)
Usuario → Permissões diretas (N:N)


---

## 7. Como a autorização funciona

### Quando um usuário tenta acessar uma rota:

1. O backend identifica o usuário pelo token JWT.
2. O sistema calcula suas permissões efetivas:
   
permissões diretas do usuário

- permissões de todos os seus papéis
3. O Request é autorizado ou negado.

### 7.1 Permissão total (superuser)

Se `user.is_superuser == True`, o RBAC **é ignorado**.

---

## 8. Regras de Negócio

1. Nenhum usuário sem papéis/permissões acessa áreas restritas.  
2. Papéis definem perfis operacionais completos.  
3. Alterações em papéis impactam todos os usuários que os utilizam.  
4. Um usuário pode ter múltiplos papéis.  
5. Permissões diretas prevalecem sobre permissões de papéis.  
6. Superusers ignoram toda verificação de RBAC.  
7. Permissões devem ser criadas e gerenciadas apenas por administradores.  

---

## 9. Fluxos de Negócio

### 9.1 Atribuição de Papéis a Usuários

Fluxo:

1. Administrador abre o perfil do usuário.  
2. Seleciona um ou mais papéis.  
3. Sistema recalcula automaticamente permissões efetivas.  

---

### 9.2 Criação de um Papel

1. Administrador define nome e descrição.  
2. Seleciona as permissões que o papel terá.  
3. Salva o papel.  
4. O papel passa a estar disponível para usuários.

---

### 9.3 Atribuir Permissão Direta ao Usuário

Utilizado em casos excepcionais:

- permissões temporárias  
- substituições  
- acesso emergencial  

Não é recomendado para uso contínuo.

---

### 9.4 Autorização de Rotas (DRF)

Cada rota deve declarar a permissão necessária.

Exemplo DRF:

```python
class UsuarioListView(APIView):
 permission_required = "core.usuarios.listar"
```
Middleware verificará automaticamente.

## 10. Endpoints (API)
Base: `/api/core/rbac/`

### 10.1 Permissões

**GET** `/permissoes/`

**POST** `/permissoes/`

**PATCH** `/permissoes/{id}/`

**DELETE** `/permissoes/{id}/ (soft delete)`

### 10.2 Papéis

**GET** `/papeis/`

**POST** `/papeis/`

**PATCH** `/papeis/{id}/`

**DELETE** `/papeis/{id}/`

### 10.3 Atribuições

**POST** `/usuarios/{id}/papeis/`

**POST** `/usuarios/{id}/permissoes/`

## 11. Erros e Exceções
Código	Mensagem	                    Motivo
403	    Acesso negado	                Usuário sem permissão necessária
403	    Requer permissão                administrativa	Alteração restrita
404	    Papel não encontrado	        ID inválido
404	    Permissão não encontrada	    ID inválido
409	    Permissão já atribuída ao papel	Duplicidade
409	    Papel já atribuído ao usuário	Duplicidade

## 12. Observações Técnicas

- O RBAC deve estar acoplado ao Django REST Framework via permission classes.
- O sistema deve carregar permissões durante o login JWT.
- O frontend deve ocultar menus baseado no RBAC.
- Papéis podem ser exportados/importados para replicar ambientes.
- Soft Delete preserva histórico de mudanças.