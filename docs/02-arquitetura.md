# Arquitetura do Sistema — Sigflor

## 1. Visão Geral da Arquitetura

O Sigflor utiliza uma arquitetura **separada entre frontend e backend**, garantindo desacoplamento, escalabilidade e facilidade de manutenção.  

- O **frontend** é desenvolvido em **React**, responsável pela camada de apresentação.
- O **backend** utiliza **Django + Django REST Framework (DRF)**, responsável pela camada de API, regras de negócio, persistência e integrações.
- A comunicação entre frontend e backend é realizada via **API REST**, com autenticação baseada em **JWT**.

Esta arquitetura foi definida para permitir flexibilidade, modularidade e expansão gradual sem comprometer desempenho ou organização interna.

---

## 2. Backend: Estrutura em Camadas

O backend segue um padrão claro de separação de responsabilidades, baseado em uma arquitetura em camadas:
- views → serializers → services → selectors → models

### 2.1 Views (Viewsets)
- Responsáveis por coordenar request/response.
- Não contêm lógica de negócio.
- Chamam selectors e services conforme necessário.
- São expostas como endpoints REST utilizando o DRF.

### 2.2 Serializers
- Realizam validações de entrada e saída.
- Transformam dados para/da API.
- Não devem conter lógica complexa.
- Podem chamar pequenos métodos utilitários, mas nunca regras de negócio.

### 2.3 Services
- Camada onde ficam todas as **regras de negócio**.
- Implementam fluxos como:
  - criação de funcionários,
  - geração de matrícula,
  - controle de patrimônio,
  - movimentações de estoque,
  - registro de manutenção,
  - criação de contratos/subcontratos.
- São facilmente testáveis pois ficam isolados das views.

### 2.4 Selectors
- Camada responsável por consultas otimizadas.
- Centralizam queries complexas.
- Evitam N+1 problemas usando `select_related` e `prefetch_related`.
- Exemplo: obter frota com status, últimas manutenções e documentos.

### 2.5 Models
- Contêm a estrutura de dados (ORM).
- Incluem campos, constraints, relacionamentos.
- Utilizam **Soft Delete** em todo o sistema.

### 2.6 Soft Delete Global
- Nenhum registro é removido definitivamente.
- Todos os modelos herdam de um `SoftDeleteModel`.
- Permite:
  - histórico completo,
  - auditorias,
  - rastreabilidade,
  - recuperação de dados excluídos indevidamente.

---

## 3. Organização dos Módulos (Apps)

O Sigflor é organizado por domínios, garantindo clareza e modularidade.

Exemplo de organização:
- apps/
- core/
- patrimonio/
- frota/
- manutencao/
- operacoes/
- suprimentos/
- compras/
- financeiro/
- rh/
- auditoria/
- indicadores/
- documentos/

Cada módulo contém suas próprias subcamadas:
apps/<modulo>/
models/
serializers/
services/
selectors/
views/
urls/

---

## 4. Comunicação Frontend ↔ Backend

A comunicação entre React e Django REST é feita por **API REST** utilizando **JWT (JSON Web Token)**.

### 4.1 Fluxo de autenticação (JWT SimpleJWT)
- React envia usuário e senha para `/api/auth/login/`
- Backend retorna:
  - `access_token` (curta duração)
  - `refresh_token` (longa duração)
- React guarda o access token (localStorage ou memory state)
- Backend valida o token a cada requisição
- Quando o token expira, o React usa o refresh token para obter um novo

### 4.2 Formato das requisições
- Todas as rotas usam JSON.
- Permite paginação, filtros e ordenação via query parameters.
- Comunicação sempre via HTTPS.

---

## 5. Integrações Externas

Na Fase 1, está prevista a integração com:

### **iFractal**
- Integração via API para:
  - dados de ponto,
  - horários,
  - frequência,
  - atestados,
  - ocorrências,
  - banco de horas.
- O backend será responsável por:
  - coletar,
  - tratar,
  - armazenar,
  - consolidar os dados para outros módulos (RH e indicadores).

A integração será documentada em um capítulo próprio.

---

## 6. Infraestrutura

O ambiente utiliza **Docker** para padronização e facilidade de deploy.

### 6.1 Componentes do Docker
- `backend` (Django)
- `frontend` (React)
- `db` (PostgreSQL)
- `redis` (futuro, para filas e cache)
- Rede interna Docker

---

## 7. Benefícios da Arquitetura

- Fácil manutenção graças à divisão clara de responsabilidades  
- Regras de negócio isoladas e testáveis  
- Queries otimizadas garantindo performance  
- Estrutura escalável conforme surgirem novos módulos  
- Separação total entre backend e frontend  
- Flexibilidade para futuras integrações externas  
- Baixo acoplamento e alta coerência em cada módulo  

---