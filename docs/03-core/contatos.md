# Módulo Core — Contatos (Entidade Genérica)

## 1. Visão Geral

O módulo **Contatos** fornece uma estrutura genérica e reutilizável para armazenar informações de contato associadas a qualquer entidade do Sigflor.

Ele utiliza **GenericForeignKey**, permitindo que contatos sejam vinculados a:

- Pessoa Física  
- Pessoa Jurídica  
- Empresas  
- Contratantes  
- Fornecedores  
- Funcionários  
- Departamentos (se aplicável)  
- Patrimônios  
- Frota  
- Unidades Operacionais  

Usuários **não manipulam contatos diretamente via CORE**.  
Eles sempre são criados/alterados **pelos módulos que os utilizam**, como:

- RH  
- Compras  
- Empresas  
- Contratantes  

A entidade de contatos é flexível e suporta diferentes tipos (telefone celular, telefone fixo, e-mail, outros), com validações fortes centralizadas no `ContatosValidator`.

---

## 2. Entidade: Contato (implementação real)

### 2.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|------------|
| id | UUID (herdado) | Sim | Identificador único |
| tipo | enum | Sim | Tipo de contato (celular, fixo, email, outro) |
| valor | string (150) | Sim | Conteúdo do contato (telefone ou e-mail) |
| principal | boolean | Sim (default=False) | Indica se é o contato principal daquele tipo |
| content_type | FK ContentType | Sim | Modelo vinculado |
| object_id | bigint | Sim | ID da entidade vinculada |
| entidade | GenericForeignKey | Sim | Entidade vinculada |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Usuário criador |
| updated_by | FK usuário | Não | Último editor |

---

## 3. Tipos de Contato (Enum)

A enumeração `Tipo` contém:

| Valor | Descrição |
|-------|-----------|
| telefone_celular | Telefone Celular |
| telefone_fixo | Telefone Fixo |
| email | E-mail |
| outro | Outro |

Esses valores controlam:
- validação aplicada  
- formatação  
- unicidade por tipo/entidade  
- visualização  

---

## 4. Regras de Negócio (Baseadas no modelo real)

1. **Contatos nunca são cadastrados diretamente no CORE**.  
   São sempre criados por módulos dependentes.

2. Um contato é único por:  
   - entidade  
   - tipo  
   - valor  
   Garantido por:

```Python
UniqueConstraint(
    fields=['content_type', 'object_id', 'tipo', 'valor'],
    name='uniq_contatos_tipo_valor_entidade'
)
```

3. Cada entidade pode ter apenas um contato principal por tipo, garantido por:
```Python
UniqueConstraint(
    fields=['content_type', 'object_id', 'tipo'],
    condition=Q(principal=True),
    name='uniq_contato_principal_por_tipo_entidade'
)
```

4. A normalização e validação do valor dependem do tipo:
- EMAIL → ContatosValidator.normalizar_email
- FIXO → ContatosValidator.normalizar_telefone_fixo
- CELULAR → ContatosValidator.normalizar_telefone_celular
- OUTRO → apenas strip()

## 5. Validações Automáticas (via clean)
O método clean() executa:
```Python
if tipo == EMAIL:
    normalizar email
elif tipo == FIXO:
    normalizar fixo (sem máscara)
elif tipo == CELULAR:
    normalizar celular (sem máscara)
else:
    strip()
```
E o método save() chama full_clean() garantindo:
-normalização
-validação do tipo
-verificação dos constraints

## 6. Formatação automática para exibição
A propriedade valor_formatado transforma:

Telefone celular (11 dígitos):
(67) 99999-1234

Telefone fixo (10 dígitos):
(67) 3345-6789

Emails e outros contatos não recebem formatação.

## 7. Fluxos de Negócio (Indiretos)

Os seguintes fluxos ocorrem via módulos dependentes:

### 7.1 Cadastro de fornecedor
- Usuário informa e-mail e telefone do fornecedor.
- O módulo cria Pessoa Jurídica.
- Módulo chama ContatoService.
- Os contatos são criados e vinculados.

### 7.2 Cadastro de funcionário
- RH registra funcionário.
- Dados de telefone e e-mail são enviados ao service de contatos.
- Validação e normalização são aplicadas.

### 7.3 Atualização de contato principal
- Módulo dependente define novo contato principal.
- O constraint garante exclusividade.
- Logs são gravados.

### 7.4 Remoção
Soft delete via módulo dependente.

## 8. Endpoints (API) — Internos

- Base: `/api/internal/contatos/`
Apenas módulos internos podem usar.

### 8.1 Criar

**POST** `/api/internal/contatos/`
Body básico:
```JSON
{
  "tipo": "email",
  "valor": "financeiro@empresa.com",
  "principal": true,
  "content_type": "pessoa_juridica",
  "object_id": 8
}
```
### 8.2 Atualizar

**PATCH** `/api/internal/contatos/{id}/`

### 8.3 Listar por entidade

**GET** `/api/internal/contatos/?content_type=<modelo>&object_id=<id>`

### 8.4 Excluir (Soft Delete)

**DELETE** `/api/internal/contatos/{id}/`

## 9. Erros e Exceções
Código	Mensagem	                            Motivo
400	    Tipo inválido	                        Valor fora da enum
400	    Telefone inválido	                    Normalização falhou
400	    Email inválido	                        Validação falhou
400	    Contato duplicado	                    Violação do UniqueConstraint
403	    Endpoint interno	                    Acesso negado
404	    Contato não encontrado	                ID inválido
409	    Já existe contato principal desse tipo	Violação do constraint principal

## 10. Observações Técnicas
- Sempre usar service layer para criar e atualizar contatos.
- Telefones SEMPRE armazenados sem formatação.
- Emails são normalizados (lowercase, trim, etc).
- O módulo usa indexes para performance em consultas.
- O campo “principal” é exclusivo por tipo/entidade.
- valor_formatado evita repetir lógica no frontend.