# Módulo Core — Anexos (Genérico)

## 1. Visão Geral

O submódulo **Anexos** é responsável pelo armazenamento de arquivos complementares, de natureza menos formal do que os documentos categorizados no módulo **Documentos**.

Enquanto *Documentos* tratam de arquivos formais, certificados e juridicamente relevantes, os **Anexos** servem para:

- imagens  
- fotos operacionais  
- prints  
- laudos complementares  
- comprovantes auxiliares  
- PDFs ou arquivos vinculados a operações cotidianas  
- anexos de chamados, solicitações, inspeções e ocorrências  

Esse módulo é genérico e pode ser vinculado a qualquer entidade do sistema.

---

## 2. Objetivo do Submódulo

O submódulo foi criado para:

- permitir upload ilimitado de arquivos a qualquer entidade  
- separar arquivos auxiliares dos documentos formais  
- padronizar armazenamento genérico  
- facilitar anexação de mídias e arquivos operacionais  
- manter auditoria e histórico completos  
- permitir rápido envio e associação de arquivos  

---

## 3. Quando usar Documentos e quando usar Anexos?

| Uso | Documentos | Anexos |
|------|-----------|--------|
| Arquivos formais | ✔ | – |
| Documentos com validade | ✔ | – |
| Arquivos que precisam de “tipo” | ✔ | – |
| Arquivos que podem ser múltiplos sem classificação | – | ✔ |
| Fotos, prints, relatórios rápidos | – | ✔ |
| Uploads feitos por campo/produção | – | ✔ |
| Comprovantes complementares | – | ✔ |
| Múltiplos arquivos por item | – | ✔ |

---

## 4. Entidade: Anexo

### 4.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|--------|------|-------------|-----------|
| id | UUID | Sim | Identificador único |
| nome_original | string | Sim | Nome original do arquivo enviado |
| arquivo | FileField | Sim | Caminho do arquivo armazenado |
| descricao | text | Não | Observações extras |
| content_type | FK → ContentType | Sim | Entidade relacionada |
| object_id | bigint | Sim | ID da entidade |
| entidade | GenericForeignKey | Sim | Referência direta |
| tamanho | bigint | Sim | Tamanho do arquivo em bytes |
| mimetype | string | Sim | Tipo MIME detectado |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |

---

## 5. Relacionamentos

### 5.1 Relacionamento Genérico

Através de `content_type` e `object_id`, um Anexo pode ser vinculado a:

- Pessoa Física  
- Pessoa Jurídica  
- Funcionário  
- Empresas do Grupo  
- Frota  
- Patrimônio  
- Atividades Operacionais  
- Chamados / Ocorrências  
- Compras (solicitações, pedidos)  
- Manutenções  
- Contratos  
- Financeiro  
- Produção  

### 5.2 Multiplicidade

- Uma entidade pode ter **N anexos**  
- Diferente dos documentos, anexos **não têm tipo**  
- Não existe controle de “principal”

---

## 6. Regras de Negócio

1. O arquivo deve ser válido de acordo com:
   - mimetype permitido  
   - tamanho máximo (definido no CORE ou nas configs globais)  
2. Soft delete sempre aplicado.  
3. O arquivo deve ser armazenado no storage oficial.  
4. Download deve exigir autenticação via RBAC.  
5. Upload pode ser liberado por perfis operacionais (ex.: supervisores de campo).  
6. Anexos não devem substituir documentos formais.  
7. Anexos não possuem classificação por tipo.

---

## 7. Fluxos de Negócio

### 7.1 Upload de Anexo

1. Usuário seleciona o arquivo.  
2. O backend valida:
   - extensão  
   - mimetype  
   - tamanho  
3. O arquivo é armazenado.  
4. Auditoria registra o upload.  
5. Retorna metadados do anexo.

---

### 7.2 Download de Anexo

- Apenas usuários autorizados pelo RBAC podem baixar.
- O link deve ser temporário (storage signed URL) quando aplicável.

---

### 7.3 Exclusão

- Exclusão sempre lógica (`deleted_at` setado).
- O arquivo permanece no storage até rotinas internas de limpeza.

---

### 7.4 Visualização Inline

Para tipos de arquivo como:

- `.jpg`  
- `.png`  
- `.pdf`

o sistema deve permitir pré-visualização (preview) no próprio frontend.

---

## 8. Metadados Salvos Automaticamente

Ao realizar upload, o sistema deve extrair:

- nome original  
- extensão  
- tamanho do arquivo  
- mimetype detectado  
- hash do arquivo (opcional para detecção de duplicidade)

---

## 9. Endpoints (API)

### Base
`/api/core/anexos/`


---

### 9.1 Listar anexos

**GET** `/api/core/anexos/`

Filtros possíveis:

- entidade_tipo  
- entidade_id  
- mimetype  
- tamanho  
- busca textual  

---

### 9.2 Obter anexo

**GET** `/api/core/anexos/{id}/`

Inclui:

- metadados  
- URL segura para download  
- entidade vinculada  

---

### 9.3 Upload

**POST** `/api/core/anexos/`

Exemplo:

```json
{
  "content_type": "atividade_operacional",
  "object_id": "e3fc8d09-4a1e-47dd-83ea-1b3b6aa4f0c2",
  "descricao": "Foto da operação realizada"
}
```


---

### 9.1 Listar anexos

**GET** `/api/core/anexos/`

Filtros possíveis:

- entidade_tipo  
- entidade_id  
- mimetype  
- tamanho  
- busca textual  

---

### 9.2 Obter anexo

**GET** `/api/core/anexos/{id}/`

Inclui:

- metadados  
- URL segura para download  
- entidade vinculada  

---

### 9.3 Upload

**POST** `/api/core/anexos/`

Exemplo:

```json
{
  "content_type": "atividade_operacional",
  "object_id": "e3fc8d09-4a1e-47dd-83ea-1b3b6aa4f0c2",
  "descricao": "Foto da operação realizada"
}
```
Arquivo é enviado no campo multipart arquivo.

## 9.4 Atualizar (metadados apenas)

**PATCH** `/api/core/anexos/{id}/`

## 9.5 Excluir (soft delete)

**DELETE** `/api/core/anexos/{id}/`

## 10. Erros e Exceções
Código	Mensagem	            Motivo
400	    Arquivo inválido	    Mimetype/extensão/tamanho
400	    Content Type inválido	Entidade não registrada
404	    Anexo não encontrado	ID inexistente
403	    Acesso negado	        Falta de permissões
413	    Arquivo muito grande	Excede limite configurado


## 11. Observações Técnicas

- Deve usar o mesmo backend de storage configurado para Documentos.
- O tamanho máximo pode ser configurável no módulo de Parâmetros Globais.
- Permitir upload simultâneo (multi-upload).
- Armazenar hash do arquivo facilita deduplicação.
- Pode ser integrado ao módulo de auditoria avançada.
- Não deve ter vínculo com lógica de validade — diferente do módulo Documentos.