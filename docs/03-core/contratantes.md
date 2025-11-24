# Módulo Core — Contratantes

## 1. Visão Geral

O submódulo **Contratantes** representa todas as empresas responsáveis pela contratação dos serviços da organização.  
Ele é um cadastro corporativo central, utilizado pelos módulos de:

- Contratos e Subcontratos  
- Financeiro  
- Operações  
- Compras (quando houver relação comercial reversa)  
- Indicadores e Auditoria  

Um Contratante é, essencialmente, uma **Pessoa Jurídica classificada como cliente contratante**.  
Por isso, este módulo depende diretamente do submódulo **Pessoa Jurídica** do CORE.

---

## 2. Objetivo do Submódulo

O propósito principal do módulo é:

- Registrar empresas que contratarão serviços da organização  
- Centralizar informações jurídicas dessas empresas  
- Manter relação com endereços e contatos  
- Disponibilizar dados para criação de contratos  
- Permitir ativação/desativação sem perda de histórico  
- Garantir consistência através de validação única via Pessoa Jurídica  

---

## 3. Entidade: Contratante

### 3.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador único |
| pessoa_juridica | FK → PessoaJuridica | Sim | Dados legais da empresa |
| descricao | text | Não | Observações complementares |
| ativo | boolean | Sim (default=True) | Indica se o contratante está ativo |
| enderecos | GenericRelation | Não | Endereços associados |
| contatos | GenericRelation | Não | Contatos associados |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Criador |
| updated_by | FK usuário | Não | Último editor |

---

## 4. Relacionamentos

- **1:1 com Pessoa Jurídica**  
  Cada Contratante representa exatamente uma Pessoa Jurídica.  
  O inverso também é verdade (uma PJ só pode ser um Contratante por vez).

- **GenericRelation para Endereços e Contatos**  
  Permite múltiplos endereços e contatos sem duplicar estrutura.

- Reverso:
pessoa_juridica.contratante → Contratante


---

## 5. Regras de Negócio

1. Todo Contratante deve estar vinculado a uma Pessoa Jurídica válida e ativa.  

2. Apenas uma instância de Contratante pode existir por Pessoa Jurídica.  
   Garantido pelo constraint de unicidade.

3. O Contratante pode estar **ativo ou inativo**:  
   - ativo = aparece em cadastros e contratos novos  
   - inativo = preservado para histórico, mas não selecionável em novos fluxos  

4. Exclusão é sempre soft delete.  

5. A edição permite atualização de:
   - status ativo/inativo  
   - descrição  
   - endereços e contatos via generic relation  

6. Campos sensíveis da Pessoa Jurídica (CNPJ, razão social) só podem ser alterados através do módulo Pessoa Jurídica.

---

## 6. Fluxos Principais

### 6.1 Cadastro de Contratante

**Atores:** Administrativo, Gestão, Contratos  
**Pré-condição:** Pessoa Jurídica existente ou criação automática via payload

**Fluxo:**
1. Usuário informa dados jurídicos da empresa.  
2. O sistema cria ou reutiliza a Pessoa Jurídica.  
3. O Contratante é criado e vinculado à PJ.  
4. Usuário adiciona endereços e contatos.  
5. Registro de auditoria é gerado.

---

### 6.2 Atualização

Usuário pode alterar:

- descrição  
- contatos  
- endereços  
- status ativo/inativo  

### 6.3 Desativação

- Marca o Contratante como `ativo=False`  
- Preserva histórico em contratos  
- Não permite remoção física  

---

## 7. Endpoints (API)

### Base
`/api/internal/contratantes/`


---

### 7.1 Listar

**GET** `/api/internal/contratantes/`

Filtros possíveis:
- `ativo=true|false`
- `cnpj`
- `razao_social`
- `search`

---

### 7.2 Obter por ID

**GET** `/api/internal/contratantes/{id}/`

---

### 7.3 Criar Contratante

**POST** `/api/internal/contratantes/`

Exemplo:

```json
{
  "pessoa_juridica": {
    "razao_social": "Green Woods Agroflorestal LTDA",
    "nome_fantasia": "GreenWoods",
    "cnpj": "12345678000199"
  },
  "descricao": "Cliente responsável pelo bloco norte da operação",
  "ativo": true
}
```
Backend deve:
- Criar ou reutilizar Pessoa Jurídica
- Criar Contratante
- Permitir endereços e contatos em payloads aninhados (opcional)

### 7.4 Editar Contratante

**PATCH** `/api/internal/contratantes/{id}/`

### 7.5 Alterar status (ativar/desativar)
```json
{
  "ativo": false
}
```

### 7.6 Excluir (Soft Delete)

**DELETE** `/api/internal/contratantes/{id}/`

## 8. Erros e Exceções
Código	Mensagem	                        Motivo
400	    Pessoa Jurídica inválida	        Dados insuficientes
400	    CNPJ já utilizado	                PJ já registrada e vinculada
404	    Contratante não encontrado	        ID inexistente
409	    PJ já vinculada a outro contratante	Unicidade 1:1
403	    Sem permissão	                    Usuário sem acesso

## 9. Observações Técnicas
- O módulo depende integralmente de Pessoa Jurídica.
- Apoia-se em GenericRelation para contatos e endereços.
- Toda criação e edição deve ser feita pela service layer.
- A inativação não remove histórico de subcontratos, contratos ou dados financeiros.
- A PK é UUID e o soft delete é obrigatório.