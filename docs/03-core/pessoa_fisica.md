# Módulo Core — Pessoa Física

## 1. Visão Geral

A entidade **Pessoa Física** é um cadastro **técnico**, não acessível diretamente ao usuário final.  
Ela funciona como **estrutura básica e unificada** para todos os módulos que lidam com indivíduos, evitando duplicação de dados e inconsistências.

Usuários **não criam** uma pessoa física diretamente.  
Em vez disso, módulos dependentes realizam essa tarefa automaticamente:

- Módulo de RH → Funcionários, Dependentes  
- Módulo Financeiro → Responsáveis por autorizações  
- Módulo de Compras → Representantes de fornecedores (opcional)  
- Módulo de Contratos → Responsáveis legais  

Cada módulo que exige pessoa física se responsabiliza por criar, atualizar e manter os dados desta entidade.

---

## 2. Papel da Pessoa Física no Sistema

### 2.1 O que ela representa
Um cadastro padronizado contendo apenas **informações pessoais fundamentais**, sem vínculo funcional ou organizacional.

### 2.2 Por que fica no CORE?
- Para ser reutilizada por vários módulos  
- Para manter consistência e evitar duplicação  
- Para facilitar integrações e validações centralizadas  
- Para permitir controle único de documentos, contatos e endereços

---

## 3. Entidade: Pessoa Física

### 3.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|------------|
| id | UUID | Sim | Identificador único |
| nome_completo | string | Sim | Nome completo |
| cpf | string | Sim, único | Documento oficial |
| rg | string | Não | RG |
| orgao_emissor | string | Não | Emissor do RG |
| data_nascimento | date | Não | Data de nascimento |
| sexo | enum | Não | M, F, Outro |
| estado_civil | enum | Não | Solteiro, Casado, etc. |
| nacionalidade | string | Não | Nacionalidade |
| naturalidade | string | Não | Cidade/estado |
| observacoes | text | Não | Informações adicionais |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Criador |
| updated_by | FK usuário | Não | Último editor |

---

### 3.2 Relacionamentos

| Relacionamento | Tipo | Descrição |
|----------------|------|-----------|
| enderecos | GenericRelation | Endereços da pessoa |
| contatos | GenericRelation | Telefones e emails |
| documentos | GenericRelation | Documentos pessoais |
| anexos | GenericRelation | Imagens, fotos, comprovantes |

---

## 4. Regras de Negócio

1. **A Pessoa Física não é criada pelo usuário.**  
   Ela é criada automaticamente quando um módulo (ex.: RH) cria uma entidade que depende dela.

2. Cada módulo é responsável por **validar os dados antes de criar ou atualizar** a pessoa física.

3. Um CPF só pode existir uma vez no sistema.

4. Se um módulo tentar criar uma nova pessoa usando um CPF já existente, o sistema deve:
   - utilizar o cadastro existente **ou**  
   - retornar erro de conflito, dependendo da regra de negócio definida.

5. Alterações de dados sensíveis (CPF, RG) devem:
   - exigir permissão especial  
   - registrar log detalhado  
   - propagar atualização para entidades dependentes, se necessário

6. O CPF deve ser:
   - único no sistema  
   - validado pelo algoritmo de CPF  
   - salvo sem formatação (`"12345678910"`)

7. A exclusão é sempre soft delete.

---

## 5. Fluxos de Negócio (Indiretos)

### 5.1 Criação indireta — via Funcionário (exemplo)

**Atores:** RH  
**Módulo:** RH → Funcionário  

**Fluxo:**
1. RH inicia cadastro de Funcionário.  
2. Preenche dados pessoais básicos.  
3. O módulo RH envia esses dados ao serviço `PessoaFisicaService`.  
4. A pessoa física é criada (ou reutilizada).  
5. O funcionário é vinculado à pessoa física.  

---

### 5.2 Atualização indireta — via módulos dependentes

Qualquer módulo que edite dados pessoais deve:

1. Carregar pessoa física existente  
2. Validar permissões  
3. Atualizar apenas os campos permitidos  
4. Registrar auditoria detalhada  

---

### 5.3 Consulta indireta

Usuários podem visualizar dados pessoais **apenas dentro do contexto** do módulo onde têm permissão.

Exemplo:  
– RH vê dados da pessoa vinculada ao Funcionário  
– Compras vê dados do representante do fornecedor  
– Oficina não vê nada, pois não tem acesso a essa entidade

---

## 6. Endpoints (API) — **Somente para uso interno**

A API de Pessoa Física **não será exposta ao usuário**, mas estará disponível internamente.

### Base interna:
`/api/internal/pessoas-fisicas/`

Endpoints só podem ser chamados por:

- Módulos internos  
- Serviços autorizados  
- Superusuários (admin)  

### 6.1 Criar (usado por módulos dependentes)

**POST** `/api/internal/pessoas-fisicas/`

Body:
<!-- Arrumar isso aqui para como vai ser na real -->
```JSON
{
  "nome_completo": "Maria Oliveira",
  "cpf": "11122233344"
}
```

### 6.2 Buscar por CPF:

**GET** `/api/internal/pessoas-fisicas/by-cpf/{cpf}/`

### 6.3 Atualizar (restrito):

**PATCH** `/api/internal/pessoas-fisicas/{id}/`

### 6.4 Inativar (Soft Delete):

**DELETE** `/api/internal/pessoas-fisicas/{id}/`

## 7. Erros e Exceções:
Código  Mensagem	               Motivo
400	    CPF inválido	         Validação
400	    Dados insuficientes	   Módulo não enviou campos obrigatórios
403	    Acesso negado	         Endpoint interno apenas
404	    Pessoa não encontrada	ID inválido
409	    CPF já cadastrado	   Módulo tentou criar duplicado


## 8. Observações Técnicas:
- Não deve existir tela ou endpoint público de CRUD.
- O módulo deve ter serializer próprio para uso interno.
- PessoaFisicaService deve ser a única forma de criar/editar registros.
- Uso obrigatório de UUID como PK.
- Indexar CPF e nome para consultas internas.
- Campos sensíveis devem ter nível alto de auditoria.
