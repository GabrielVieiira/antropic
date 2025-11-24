# Módulo Core — Pessoa Jurídica

## 1. Visão Geral

A entidade **Pessoa Jurídica** é um cadastro **técnico e centralizado**, utilizado por diversos módulos do Sigflor.  
Ela **não é criada diretamente pelo usuário**; em vez disso, é criada automaticamente por entidades que dependem dela, como:

- Empresas (CNPJs da organização)
- Contratantes
- Fornecedores (módulo de compras)
- Transportadoras
- Prestadores de serviço
- Instituições financeiras
- Parceiros e clientes (futuro)

O objetivo é evitar duplicação de cadastros, manter consistência e garantir que todos os módulos utilizem a mesma base jurídica.

---

## 2. Papel da Pessoa Jurídica no Sistema

### 2.1 Para que serve
A Pessoa Jurídica padroniza e centraliza os dados de empresas e organizações, permitindo que qualquer módulo faça referência a ela de forma consistente.

### 2.2 Por que está no CORE
- Evita duplicação de cadastros em módulos distintos (Compras, Patrimônio, Financeiro, Suprimentos).  
- Facilita validações e auditorias.  
- Permite uso de endereços, contatos e documentos de forma genérica via GenericRelation.  
- Torna integrações externas mais simples.  
- Permite regras únicas de validação para CNPJ, IE, porte empresarial etc.

---

## 3. Entidade: Pessoa Jurídica

### 3.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|------------|
| id | UUID | Sim | Identificador único |
| razao_social | string | Sim | Nome legal da empresa |
| nome_fantasia | string | Não | Nome comercial |
| cnpj | string | Sim, único | Cadastro Nacional da Pessoa Jurídica |
| inscricao_estadual | string | Não | IE — pode ser isento |
| inscricao_municipal | string | Não | IM |
| porte | enum | Não | MEI, ME, EPP, Médio, Grande |
| natureza_juridica | string | Não | Ex.: Sociedade Limitada |
| data_abertura | date | Não | Data de registro/abertura |
| atividade_principal | string | Não | CNAE principal |
| atividades_secundarias | list[string] | Não | Lista de CNAEs |
| situacao_cadastral | string | Não | Ativa, Suspensa, Inapta, Baixada |
| observacoes | text | Não | Campo livre |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Criador |
| updated_by | FK usuário | Não | Último editor |

---

### 3.2 Relacionamentos

| Relacionamento | Tipo | Descrição |
|----------------|------|-----------|
| enderecos | GenericRelation | Endereços da empresa |
| contatos | GenericRelation | Telefones e emails |
| documentos | GenericRelation | Documentos (contratos, NF, certidões) |
| anexos | GenericRelation | Uploads diversos |
| empresas | FK reverso | Referência para módulos que usam PJ como base |
| contratantes | FK reverso | Entidades contratantes |
| fornecedores | FK reverso | Fornecedores (módulo compras) |
| prestadores_servico | FK reverso | Serviços terceirizados |

---

## 4. Regras de Negócio

1. A Pessoa Jurídica **nunca é cadastrada diretamente pelo usuário**.  
   - Criada automaticamente através dos módulos dependentes (Empresas, Contratantes, Fornecedores etc).

2. O CNPJ deve ser:
   - único no sistema  
   - validado pelo algoritmo de CNPJ  
   - salvo sem formatação (`"12345678000199"`)

3. Atualizar dados sensíveis (CNPJ, Razão Social) exige permissão especial e gera auditoria avançada.

4. Exclusão sempre é soft delete.

5. Um módulo que tentar cadastrar PJ com CNPJ já existente:  
   - utiliza a existente **ou**  
   - retorna erro de conflito (dependendo da regra do módulo)

6. Campos como “atividade principal”, “porte” e “natureza jurídica” podem vir de:
   - input do usuário

---

## 5. Fluxos de Negócio (Indiretos)

### 5.1 Criação indireta — Exemplo: Cadastro de Empresa do Grupo

**Atores:** Administrativo / Controladoria  
**Módulo:** CORE → Empresas  
**Fluxo:**
1. Usuário preenche dados da empresa.  
2. O módulo solicita criação de Pessoa Jurídica.  
3. Validação de CNPJ.  
4. Criada e vinculada à entidade Empresa.  

---

### 5.2 Criação indireta — Exemplo: Cadastro de Fornecedor (Compras)

**Fluxo resumido:**
1. Preencher dados da empresa contratada.  
2. O módulo de compras chama `PessoaJuridicaService.create()`  
3. Pessoa jurídica criada ou reutilizada.  
4. Fornecedor vinculado ao cadastro criado.  

---

### 5.3 Atualização indireta

Somente módulos autorizados podem atualizar:
- Razão social  
- CNPJ  
- IE  
- Situação cadastral  

Cada alteração registra log com:
- usuário  
- campos alterados  
- valor anterior e novo  
- data/hora  

---

## 6. Endpoints (API) — **Uso interno**

### Base interna
`/api/internal/pessoas-juridicas/`

Apenas módulos internos podem consumir.

---

### 6.1 Criar:

**POST** `/api/internal/pessoas-juridicas/`

Body básico:
```JSON
{
  "razao_social": "Tecaflorestal LTDA",
  "cnpj": "12345678000199"
}
```

### 6.2 Buscar por CNPJ:

**GET** `/api/internal/pessoas-juridicas/by-cnpj/{cnpj}/`

### 6.3 Atualizar:

**PATCH** `/api/internal/pessoas-juridicas/{id}/`

Apenas perfis autorizados (ex.: administrador corporativo).

### 6.4 Inativar (Soft Delete):

**DELETE** `/api/internal/pessoas-juridicas/{id}/`

## 7. Erros e Exceções:
Código	Mensagem	                        Motivo
400	    CNPJ inválido	                  Validação
400	    Dados obrigatórios ausentes	   Ex.: razão social
403	    Endpoint interno	               Usuário externo tentando acessar
404	    Não encontrada	               ID inválido
409	    CNPJ já cadastrado	            PJ duplicada
409	    Não é permitido alterar CNPJ	   PJ vinculada a módulos críticos

## 8. Observações Técnicas:
- O serviço PessoaJuridicaService deve ser a única forma de criar/editar essa entidade.
- PK recomendada: UUIDField.
- Indexar CNPJ e razão social.
- Validar CNPJ com algoritmo oficial.
- Usar select_related + prefetch_related ao consultar.
- Sempre registrar logs de alterações.
- Documentos e anexos via GenericRelation.
- Nome fantasia é opcional (nem toda PJ possui).