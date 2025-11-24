# Módulo internal — Empresas (CNPJ do Grupo)

## 1. Visão Geral

O submódulo **EmpresasCNPJ** representa as empresas pertencentes ao grupo econômico da organização.  
Cada registro corresponde a um CNPJ ativo no grupo, utilizado por diversos módulos operacionais, administrativos e financeiros.

Importante:

📌 **Uma EmpresaCNPJ não armazena razão social nem CNPJ.**  
📌 **Ela é uma especialização da entidade central `Pessoa Jurídica`.**

Isso evita duplicação de dados e mantém coerência entre:

- Empresas internas  
- Contratantes  
- Fornecedores  
- Transportadoras  
- Qualquer entidade jurídica registrada no sistema  

---

## 2. Objetivo do Submódulo

- Registrar quais Pessoas Jurídicas pertencem ao grupo  
- Prover identificação empresarial nos módulos do ERP  
- Mapear CNPJs internos usados em:
  - contratos
  - faturamento
  - alocação de funcionários
  - propriedade de frota/patrimônio
  - alocação de centros de custo
- Padronizar endereços e contatos via Pessoa Jurídica  
- Garantir unicidade e integridade da estrutura organizacional

---

## 3. Entidade: EmpresaCNPJ

### 3.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador único |
| pessoa_juridica | FK → PessoaJuridica | Sim, única | Dados jurídicos associados |
| descricao | text | Não | Observações internas |
| ativa | boolean | Sim (default=True) | Indica se a empresa está ativa |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Criador |
| updated_by | FK usuário | Não | Último editor |

---

## 4. Relacionamentos

### 4.1 Relação com Pessoa Jurídica
EmpresaCNPJ 1 → 1 PessoaJuridica


Toda EmpresaCNPJ corresponde exatamente a uma Pessoa Jurídica.

### 4.2 Herança de funcionalidades via Pessoa Jurídica

Como a Pessoa Jurídica possui:

- endereços (GenericRelation)
- contatos (GenericRelation)
- documentos (GenericRelation)
- anexos (GenericRelation)

…esses dados passam automaticamente a ser os dados oficiais da EmpresaCNPJ.

### 4.3 Relacionamentos com outros módulos

- Funcionários (vínculo trabalhista → empresa empregadora)
- Frota e Patrimônio (empresa proprietária)
- Financeiro (empresa responsável por pagamentos ou recebimentos)
- Produção (empresa operacional em determinado local)
- Compras (empresa que realiza o pedido)
- Contratos (parte contratada)

---

## 5. Regras de Negócio

1. A Pessoa Jurídica vinculada deve possuir CNPJ válido e único.
2. Uma Pessoa Jurídica só pode aparecer **uma única vez** como EmpresaCNPJ.
3. Apenas **uma EmpresaCNPJ pode ser matriz**.
4. O campo `ativa` define uso operacional:
   - ativa → pode ser selecionada em módulos  
   - inativa → preservada para histórico
5. Exclusão é sempre soft delete.
6. Endereços e contatos **são gerenciados no módulo Pessoa Jurídica**, não aqui.
7. A razão social e o CNPJ **nunca são alterados aqui**, somente via Pessoa Jurídica.

---

## 6. Fluxos de Negócio

### 6.1 Cadastro de uma EmpresaCNPJ

**Fluxo:**

1. Usuário informa dados jurídicos da empresa.  
2. O sistema valida e cria (ou reutiliza) a Pessoa Jurídica.  
3. Uma EmpresaCNPJ é criada vinculada à PJ.  
4. Usuário preenche informações complementares.  

---

### 6.2 Atualização

Podem ser alterados:

- ativa/inativa  
- matriz  
- descrição  

A Pessoa Jurídica vinculada é atualizada apenas pelo módulo próprio.

---

### 6.3 Tornar Empresa Matriz

Regras:

- Somente uma empresa pode ser matriz  
- Definir uma nova matriz remove a flag da anterior  
- Auditoria registra a ação  

---

### 6.4 Exclusão (Soft Delete)

A empresa permanece no histórico, preservando:

- contratos  
- patrimônio  
- histórico de funcionários  
- registros financeiros  

---

## 7. Endpoints (API)

### Base
`/api/internal/empresas-cnpj/`


---

### 7.1 Listar Empresas

**GET** `/api/internal/empresas-cnpj/`

Filtros:
- `ativa=true|false`
- `matriz=true|false`
- `cnpj`
- `razao_social`
- `search`

> Busca de CNPJ e razão social é realizada através da Pessoa Jurídica.

---

### 7.2 Obter Empresa pelo ID

**GET** `/api/internal/empresas-cnpj/{id}/`

Retorna:
- dados da empresa  
- dados da pessoa jurídica  
- endereços  
- contatos  

---

### 7.3 Criar EmpresaCNPJ

**POST** `/api/internal/empresas-cnpj/`

Exemplo:

```json
{
  "pessoa_juridica": {
    "razao_social": "Tecaflorestal Serviços LTDA",
    "cnpj": "12345678000199"
  },
  "descricao": "Empresa principal do grupo",
  "matriz": true,
  "ativa": true
}
```

### 7.4 Atualizar

**PATCH** `/api/internal/empresas-cnpj/{id}/`

### 7.5 Excluir (Soft Delete)

**DELETE** `/api/internal/empresas-cnpj/{id}/`

## 8. Erros e Exceções
Código	Mensagem	                                       Motivo
400	   Dados de Pessoa Jurídica inválidos	            Falha de validação
400	   Já existe uma empresa matriz	                  Violação da regra
404	   Empresa não encontrada	                        ID inexistente
409	   Pessoa Jurídica já usada por outra EmpresaCNPJ	Violação da unicidade
403	   Sem permissão	                                 Acesso restrito

## 9. Observações Técnicas
- A Pessoa Jurídica é a “fonte da verdade” para dados cadastrais.
- Este módulo apenas classifica quais PJs fazem parte do grupo econômico.
- Endereços e contatos ficam sempre vinculados à Pessoa Jurídica.
- A PK é UUID e utiliza SoftDeleteModel.
- Toda lógica complexa deve estar concentrada em services, não no model.
- A validação de matriz é responsabilidade do service layer.