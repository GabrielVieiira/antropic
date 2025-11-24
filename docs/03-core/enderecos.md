# Módulo Core — Endereços (Entidade Genérica)

## 1. Visão Geral

A entidade **Endereço** é um recurso genérico, centralizado no CORE, utilizado por qualquer módulo que precise armazenar informações de localização:

- Pessoa Física  
- Pessoa Jurídica  
- Empresas  
- Contratantes  
- Fornecedores  
- Filiais / Departamentos Operacionais  
- Frota (quando aplicável)  
- Patrimônio  
- Almoxarifados  
- Oficinas  

Ela é implementada com **GenericForeignKey**, permitindo que um mesmo modelo de endereço seja reaproveitado por qualquer entidade do sistema, evitando duplicação de estrutura.

Usuários **nunca manipulam endereços diretamente**:  
eles são sempre criados ou atualizados **através dos módulos que os utilizam**.

---

## 2. Entidade: Endereço (Implementação Real)

### 2.1 Estrutura da Tabela

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|------------|
| id | UUID (herdado) | Sim | Identificador único |
| logradouro | string (200) | Sim | Rua/avenida |
| numero | string (20) | Não | Número do imóvel |
| complemento | string (100) | Não | Sala, bloco, apartamento etc. |
| bairro | string (100) | Não | Bairro |
| cidade | string (100) | Sim | Cidade |
| estado | UF (enum de 27 estados) | Sim | Unidade federativa |
| cep | string (8) | Sim | Código postal sem máscara |
| pais | string (50) | Sim (default "Brasil") | País |
| content_type | FK ContentType | Sim | Modelo vinculado |
| object_id | bigint | Sim | ID da entidade vinculada |
| entidade | GenericForeignKey | Sim | A entidade vinculada |
| principal | boolean | Sim (default False) | Indica endereço principal |
| created_at | datetime | Sim | Auditoria |
| updated_at | datetime | Sim | Auditoria |
| deleted_at | datetime | Não | Soft delete |
| created_by | FK usuário | Não | Criador |
| updated_by | FK usuário | Não | Último editor |

---

## 3. Enum UF (Estados Brasileiros)

O modelo inclui uma enumeração completa com os 27 estados:

AC, AL, AP, AM, BA,
CE, DF, ES, GO, MA,
MT, MS, MG, PA, PB,
PR, PE, PI, RJ, RN,
RS, RO, RR, SC, SP,
SE, TO


---

## 4. Regras de Negócio (Baseadas no Modelo Real)

1. **Endereço nunca é criado diretamente no CORE.**  
   Apenas módulos consumidores podem criá-lo.

2. **Soft delete não remove o registro**, mas:
   - remove o flag `principal`  
   - preserva histórico  

3. **Apenas um endereço principal é permitido por entidade**, garantido por:
```Python
UniqueConstraint(
    fields=['content_type','object_id'],
    condition=Q(principal=True),
    name='uniq_endereco_principal_por_entidade_vivo',
)
```

4. A combinação completa de endereço por entidade deve ser única entre registros ativos:
```Python
UniqueConstraint(
    fields=['content_type','object_id','logradouro','numero','complemento',
            'bairro','cidade','estado','cep','pais'],
    name='uniq_endereco_completo_por_entidade_vivo',
)
```
Isso impede duplicação acidental de endereços.

5. O método clean() chama:
EnderecoValidator.normalizar(self)
Esse validator deve:
- normalizar strings
- remover máscara de CEP
- ajustar capitalização
- aplicar regras de formato

6. O método save() usa full_clean() garantindo:
- validação de integridade
- execução de validators
- execução de normalização

7. Na exclusão (delete), o campo principal é automaticamente definido como False.

## 5. Comportamento Técnico Importante
5.1 Validações executadas sempre
Toda gravação passa obrigatoriamente por:
- `clean()`
- `EnderecoValidator.normalizar()`
- `full_clean()`
- validação dos constraints
Isso garante integridade mesmo em criação via service layer.

5.2 Campos indexados
O modelo cria índices automáticos:
- cep
- (cidade, estado)
- (content_type, object_id)
- (content_type, object_id, principal)

Isso é essencial para performance nas listagens por entidade.

## 6. Fluxos de Negócio (Indiretos)
6.1 Criação indireta (ex.: cadastro de fornecedor)
- Usuário preenche dados do fornecedor.
- Módulo de Compras cria/edita a Pessoa Jurídica.
- Se informado, os dados de endereço são enviados ao EnderecoService.
- Endereço é criado e vinculado via GenericRelation.

6.2 Alteração de endereço existente
- Usuário edita fornecedor/empresa/pessoa.
- Módulo chama o service de endereço.
- Os dados são normalizados pelo validator.
- O endereço é atualizado.
- Auditoria registra alterações (campo por campo).

6.3 Alterar endereço principal
- Módulo solicita troca de endereço principal.
- Registrar o novo como principal=True.
- O constraint interno força que o anterior seja ajustado.
- Auditoria registra a troca.

## 7. Endpoints (API) — Internos
Base: `/api/internal/enderecos/`

7.1 Criar:
- POST `/api/internal/enderecos/`

Body básico:
```JSON
{
  "logradouro": "Rua Machado de Assis",
  "numero": "450",
  "bairro": "Centro",
  "cidade": "Campo Grande",
  "estado": "MS",
  "cep": "79001000",
  "pais": "Brasil",
  "principal": true,
  "content_type": "pessoa_juridica",
  "object_id": 12
}
```

7.2 Atualizar:

**PATCH** `/api/internal/enderecos/{id}/`

7.3 Listar por entidade:

**GET** `/api/internal/enderecos/?content_type=<modelo>&object_id=<id>`

7.4 Excluir (Soft Delete):

**DELETE** `/api/internal/enderecos/{id}/`

## 8. Erros e Exceções
Código	Mensagem	                              Motivo
400	    Campos obrigatórios ausentes	          Logradouro, cidade, estado, cep
400	    Violação de constraint	                Endereço duplicado
400	    UF inválida	                            Estado não pertence ao enum
403	    Endpoint interno	                      Acesso não permitido
404	    Endereço não encontrado	                ID inexistente
409	    Apenas um endereço principal permitido	Violação ao constraint uniq_endereco_principal_por_entidade_vivo

## 9. Observações Técnicas

- Sempre usar services para criar/alterar endereços — nunca diretamente pelo ORM.
- O campo pais tem default "Brasil".
- CEP sempre sem máscara (8 dígitos numéricos).
- Soft delete redefine principal=False.
- Ao alterar endereço principal, UniqueConstraint garante consistência.
- O EnderecoValidator deve centralizar validações e normalizações.
