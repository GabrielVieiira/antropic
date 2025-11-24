# Módulo Core — Documentos (Genérico)

## 1. Visão Geral

O submódulo **Documentos** fornece uma estrutura genérica para armazenar e associar documentos a qualquer entidade do sistema.

Esse módulo é fundamental para garantir:

- padronização do armazenamento de documentos,
- rastreabilidade de arquivos anexados,
- separação clara entre dados estruturados e documentos físicos,
- centralização da lógica de uploads,
- compatibilidade com diversas entidades (Pessoa Física, Pessoa Jurídica, Contratantes, EmpresasCNPJ, Funcionários, Frota, Patrimônio, Contratos etc.).

---

## 2. Objetivo do Submódulo

- Permitir que qualquer entidade do ERP tenha documentos associados.  
- Unificar regras de validação e estrutura de arquivos.  
- Armazenar documentos críticos (contratos, RG, CNH, notas fiscais, comprovantes).  
- Oferecer auditoria e histórico consistente.  
- Permitir múltiplos documentos por entidade.  
- Integrar com o módulo de **Anexos**, quando necessário (ex.: arquivos adicionais).

---

## 3. Entidade: Documento

A entidade Documento é genérica e pode ser vinculada a qualquer outra entidade do sistema através do ContentType Framework.

### 3.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | UUID | Sim | Identificador único |
| tipo | string (50) | Sim | Categoria/tipo do documento |
| descricao | text | Não | Observações complementares |
| arquivo | FileField | Sim | Arquivo físico armazenado |
| content_type | FK → ContentType | Sim | Entidade relacionada |
| object_id | bigint | Sim | ID da entidade específica |
| entidade | GenericForeignKey | Sim | Referência direta |
| data_emissao | date | Não | Data de emissão do documento |
| data_validade | date | Não | Validade (ex.: CNH, ASO) |
| principal | boolean | Sim (default=False) | Documento principal por tipo |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |

---

## 4. Relacionamentos

### 4.1 Assinatura Genérica
Documento → (qualquer entidade)


Através de `content_type` / `object_id`.

### 4.2 Exemplos de uso

| Entidade | Uso do Documento |
|----------|------------------|
| Pessoa Física | RG, CPF, CNH, ASO, comprovante |
| Pessoa Jurídica | Contrato social, CNPJ escaneado |
| Funcionário | Documentos admissionais |
| Contratos | Arquivos de contrato, aditivos |
| Frota | CRLV, laudos, notas |
| Patrimônio | Nota fiscal, certificado |
| Compras | Nota fiscal digitalizada |

---

## 5. Regras de Negócio

1. O documento deve sempre estar vinculado a uma entidade.  
2. Apenas um documento do mesmo **tipo** pode ser marcado como **principal** para uma mesma entidade.  
3. O arquivo deve ser válido segundo as regras de upload (mimetype, tamanho, extensão).  
4. O sistema deve suportar múltiplos tipos de documento por entidade.  
5. Soft Delete é aplicado (o arquivo não é removido fisicamente por padrão).  
6. Documentos principais são substituídos automaticamente ao marcar um novo `principal=True`.

---

## 6. Tipos de Documento

A lista de tipos pode ser configurada via Parâmetros Globais, mas recomenda-se uma estrutura inicial:

- `identidade`
- `cpf`
- `cnh`
- `contrato_social`
- `comprovante_endereco`
- `nota_fiscal`
- `aso`
- `laudo`
- `manual`
- `contrato`
- `aditivo`
- `crlv`
- `outro`

Cada módulo pode definir seus tipos permitidos através de validações específicas na service layer.

---

## 7. Fluxos de Negócio

### 7.1 Upload de Documento

1. Usuário seleciona o tipo e o arquivo.  
2. O backend valida:
   - mimetype  
   - tamanho  
   - extensão  
   - unicidade de documento principal  
3. O arquivo é salvo no storage configurado.  
4. Auditoria registra o upload.

---

### 7.2 Substituição do Documento Principal

Quando enviado `principal = true`:

- o sistema encontra outro documento do mesmo tipo  
- marca como `principal = false`  
- salva o novo documento como principal

---

### 7.3 Exclusão de Documento

A exclusão é sempre lógica:

- marca `deleted_at`  
- o arquivo é mantido (pode ser limpo em rotinas de manutenção)

---

### 7.4 Download

O arquivo é entregue diretamente do storage via link seguro, com:

- autenticação  
- expiração  
- autorização por permissões (RBAC)

---

### 7.5 Filtragem

O frontend pode filtrar documentos por:

- tipo  
- principal  
- validade  
- data de vencimento (ex.: CNH)  
- entidade vinculada  

---

## 8. Endpoints (API)

### Base
`/api/core/documentos/`


---

### 8.1 Listar Documentos

**GET** `/api/core/documentos/`

Filtros:

- `entidade_id`
- `entidade_tipo`
- `tipo`
- `principal`
- `validade_vencida=true|false`

---

### 8.2 Obter Documento por ID

**GET** `/api/core/documentos/{id}/`

---

### 8.3 Upload

**POST** `/api/core/documentos/`

Payload multipart-exemplo:

```json
{
  "tipo": "contrato_social",
  "descricao": "Contrato social atualizado",
  "content_type": "pessoa_juridica",
  "object_id": "42",
  "principal": true,
  "data_emissao": "2020-05-12",
  "data_validade": null
}
```
Arquivo é enviado como campo arquivo.

### 8.4 Atualizar

**PATCH** `/api/core/documentos/{id}/`

### 8.5 Excluir (Soft Delete)

**DELETE** `/api/core/documentos/{id}/`

## 9. Erros e Exceções
Código	Mensagem	                    Motivo
400	    Tipo de documento inválido	    Tipo não permitido
400	    Arquivo inválido	            Mimetype/tamanho
404	    Entidade não encontrada	        content_type + object_id inválidos
409	    Documento principal já existe	Violação de unicidade
403	    Sem permissão	                Falta de permissão no RBAC

## 10. Observações Técnicas
- O módulo deve depender do storage configurado (local, S3, GCS, MinIO).
- O arquivo não é removido fisicamente por padrão.
- Toda lógica complexa de upload deve estar na service layer.
- O campo principal deve ser validado via QuerySet atômico (transação).
- Documentos podem ser usados em validações externas, como expiração.
- Integrado ao módulo de auditoria.