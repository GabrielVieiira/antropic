# Módulo Core — Usuários

## 1. Visão Geral

O submódulo **Usuários** é responsável pela autenticação, perfis e identificação de todos os usuários que acessam o sistema Sigflor.

Diferente de “Pessoa Física”, o usuário representa **a identidade digital** de alguém dentro do sistema, enquanto Pessoa Física é uma entidade real do mundo externo.

No Sigflor, um usuário pode ou não estar vinculado a uma Pessoa Física — o vínculo é recomendado para auditoria e relacionamento com outros módulos.

---

## 2. Objetivo do Submódulo

- Gerenciar contas de acesso ao ERP  
- Controlar autenticação e senhas  
- Definir permissões (integração direta com o módulo RBAC)  
- Registrar auditoria de ações  
- Armazenar informações mínimas sobre o usuário  
- Vínculo opcional com Pessoa Física do CORE  
- Servir como base para logs, histórico e criação de entidades  

---

## 3. Arquitetura baseada no Django Auth

O módulo utiliza como base:

- **UserModel customizado** (extensão do AbstractUser ou AbstractBaseUser)
- **Autenticação JWT (Json Web Token)**
- **Manager customizado** para criação de usuários
- **Integração com RBAC** (permissões e papéis)

---

## 4. Entidade: Usuário

Abaixo está o modelo final previsto para o Sigflor:

### 4.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador único |
| username | string | Sim, único | Nome de login |
| email | string | Sim, único | E-mail para recuperação |
| pessoa_fisica | FK → PessoaFisica | Não | Vínculo opcional |
| first_name | string | Sim | Nome |
| last_name | string | Sim | Sobrenome |
| password | hash | Sim | Senha criptografada |
| ativo | boolean | Sim (default=True) | Controla acesso |
| is_staff | boolean | Sim | Acesso ao admin |
| is_superuser | boolean | Sim | Permissões totais |
| last_login | datetime | Não | Último acesso |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |

---

## 5. Relacionamentos

### 5.1 Com Pessoa Física
Usuario → PessoaFisica (opcional)


Essa relação permite:

- associar permissões contextualizadas (ex.: funcionário)  
- exibir dados completos do usuário em auditorias  
- integrar módulos de produção e RH com identificação real  

### 5.2 Com RBAC (Permissões e Papeis)
Usuario → Papel (N:N)
Usuario → Permissões (diretas)


Detalhado no módulo `permissoes_rbac`.

---

## 6. Regras de Negócio

1. **E-mail e username devem ser únicos.**
2. O usuário pode ser vinculado a uma Pessoa Física, mas não é obrigatório.
3. A autenticação utiliza **JWT**, permitindo:
   - login  
   - refresh  
   - expiração configurável  
4. Um usuário desativado (`ativo=False`) não pode realizar login.
5. A senha deve sempre ser criptografada via `set_password`.
6. Exclusão de usuários deve seguir **soft delete** (herdado do modelo base).
7. `is_superuser` ignora permissões de RBAC.
8. Mudança de senha deve invalidar tokens prévios (configurável).

---

## 7. Fluxos de Negócio

### 7.1 Criação de Usuário

**Fluxo:**

1. Administrador acessa módulo de usuários.  
2. Preenche:
   - username  
   - email  
   - name  
   - senha (ou link para cadastro inicial)  
3. O backend:
   - valida unicidade  
   - criptografa senha  
   - cria registro  
   - vincula permissões iniciais  
4. Auditoria é registrada.

---

### 7.2 Login (JWT)

**POST** `/api/auth/login/`

Payload:

```json
{
  "username": "gabriel",
  "password": "senha123"
}
```

Resposta:
```json
{
  "access": "...token...",
  "refresh": "...token..."
}
```

### 7.3 Refresh Token

**POST** `/api/auth/refresh/`

### 7.4 Atualização de Perfil

O usuário pode editar:

- nome
- e-mail
- foto (se existir)
- senha

Não pode editar:
- permissões
- papéis
- atribuições sensíveis

### 7.5 Desativação (soft delete)
- usuário deixa de acessar o sistema
- histórico permanece
- auditoria registra o responsável

## 8. Endpoints (API)
Base
`/api/internal/usuarios/`

### 8.1 Listar usuários

GET `/api/core/usuarios/`

Filtros:
- ativo
- papel
- search
- pessoa_fisica

### 8.2 Obter usuário

**GET** `/api/core/usuarios/{id}/`

### 8.3 Criar usuário

**POST** `/api/core/usuarios/`

Exemplo:
```json
{
  "username": "joao.silva",
  "email": "joao.silva@empresa.com",
  "first_name": "João",
  "last_name": "Silva",
  "password": "SenhaForte123",
  "pessoa_fisica": "UUID opcional"
}
```

### 8.4 Atualizar usuário

**PATCH** `/api/core/usuarios/{id}/`

### 8.5 Reset de senha

**POST** `/api/core/usuarios/{id}/reset-senha/`

### 8.6 Desativar usuário

**PATCH** `/api/core/usuarios/{id}/`

```json
{
  "ativo": false
}
```

### 8.7 Excluir (Soft Delete)

**DELETE** `/api/core/usuarios/{id}/`

## 9. Erros e Exceções
Código	Mensagem	                            Motivo
400	    Username já existe	                    Unicidade
400	    E-mail já existe	                    Unicidade
403	    Permissão negada	                    RBAC
404	    Usuário não encontrado	                ID inválido
409	    Relação com Pessoa Física já utilizada	Violação de vínculo
401	    Credenciais inválidas	                Falha de login

## 10. Observações Técnicas
- O submódulo deve usar um UserModel customizado.
- Toda autenticação é baseada em JWT.
- pessoa_fisica não é obrigatório, mas recomendado.
- Usuários herdam SoftDeleteModel: exclusão nunca é física.
- Integração direta com o módulo de permissões (RBAC).
- Senhas nunca são logadas, salvas em texto plano ou exibidas.
- Auditoria registra:
    - criação
    - alterações
    - login
    - alterações de senha
    - desativação