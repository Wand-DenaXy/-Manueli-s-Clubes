<div align="center">

# ✦ Manueli's Clubes

### Plataforma SaaS full-stack de gestão de clubes com pagamentos Stripe, webhooks assíncronos, multi-tenancy e RBAC

*Criar clubes · Gerir membros · Calendário de eventos · Mapa interativo · Planos de subscrição · Notificações por email*

<img width="1000" height="500" alt="ManueliClube" src="https://github.com/user-attachments/assets/786aee57-cdbc-4be2-823b-51c221d7e4b8" />

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white" />
  <img alt="Redis" src="https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white" />
  <img alt="Celery" src="https://img.shields.io/badge/Celery-5.4-37814A?logo=celery&logoColor=white" />
  <img alt="Nuxt" src="https://img.shields.io/badge/Nuxt-3-00DC82?logo=nuxtdotjs&logoColor=white" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white" />
  <img alt="Stripe" src="https://img.shields.io/badge/Stripe-Webhooks%20+%20Checkout-635BFF?logo=stripe&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" />
  <img alt="JWT" src="https://img.shields.io/badge/Auth-JWT%20+%20Argon2-000000?logo=jsonwebtokens&logoColor=white" />
  <img alt="Tests" src="https://img.shields.io/badge/Tests-40%20passed-brightgreen?logo=pytest&logoColor=white" />
</p>

</div>

---

## Porquê este projeto?

> A maioria dos projetos de portfólio mostra um CRUD genérico.  
> Este vai **muito além** — é uma plataforma SaaS multi-tenant com pagamentos reais, webhooks Stripe processados de forma assíncrona, notificações por email, cache Redis, RBAC e 40 testes automatizados.

| Métrica | Valor |
|---------|-------|
| Endpoints REST | **34** (auth, CRUD, stats, pagamentos, webhooks, perfil, notificações) |
| Testes automatizados | **40/40 passed** (pytest + httpx) |
| Modelos ORM | **9** tabelas + **16** Pydantic schemas |
| Segurança | JWT + Argon2id + RBAC (3 roles) |
| Pagamentos | Stripe Checkout + Webhooks (subscrições recorrentes) |
| Processamento assíncrono | Celery + Redis (retry com backoff exponencial) |
| Notificações | Email SMTP (TLS) + notificações in-app em BD |
| Multi-tenancy | Isolamento de dados por organização |
| Dashboard | KPIs em tempo real + Chart.js (line + doughnut) |
| Mapa interativo | Leaflet.js com marcadores GPS dos clubes |
| Calendário | FullCalendar com inscrição em eventos (409 anti-duplicação) |
| Cache | Redis com TTL + invalidação por prefixo |
| Infraestrutura | Docker Compose (5 containers: DB + Redis + API + Worker + Frontend) |

---

## Funcionalidades

### Dashboard — KPIs e Gráficos em Tempo Real

Painel de administração com cards de métricas (clubes, utilizadores, mapas), gráfico de linha (registos mensais) e doughnut (distribuição por tipo de utilizador) — tudo alimentado pela API com cache.

<img width="1000" height="500" alt="Dashboard" src="nuxt-app/assets/images/DashboardManuel.PNG" />

---

### Gestão de Clubes — CRUD com RBAC e Multi-Tenancy

Tabela interativa com criação, edição inline e eliminação. **Permissões por role** (Admin vê tudo via `/clubesAdmin`, Gestor pode criar/editar na sua organização). Limites de criação enforced pelo plano ativo do utilizador. SweetAlert2 para confirmações.

---

### Planos & Pagamentos — Stripe Checkout + Webhooks

Página de subscrição com 3 tiers (Free · Pro · Enterprise). Pagamento via **Stripe Checkout** com subscrições recorrentes. Os **webhooks do Stripe** são recebidos pela API e processados de forma assíncrona via **Celery** — garantindo idempotência (deduplicação por `event_id`), retry automático com backoff exponencial (até 5 tentativas) e resiliência total a falhas temporárias.

Quando um pagamento falha, o sistema:
1. Reverte o utilizador para o plano Free
2. Cria uma notificação in-app na BD
3. Envia um email HTML via SMTP (TLS) a informar o utilizador

Quando um pagamento é bem-sucedido, o plano é ativado e o utilizador recebe confirmação por email e notificação in-app.

| Plano | Preço | Clubes | Mapas |
|-------|-------|--------|-------|
| Free | 0 €/mês | 3 | 1 |
| Pro | 9.99 €/mês | 15 | 20 |
| Enterprise | 29.99 €/mês | ∞ | ∞ |

---

### Mapa Interativo — Leaflet.js

Mapa dark-themed com marcadores dos clubes, painel lateral com lista de pontos e formulário para adicionar novas localizações por coordenadas GPS.

<img width="1000" height="500" alt="Mapas" src="nuxt-app/assets/images/ManuelMapas.PNG" />

---

### Calendário de Eventos — FullCalendar

Calendário mensal com eventos dos clubes em cores diferentes. Clicar num evento abre um painel com detalhes e botão "Ingressar" — inscrição com proteção de duplicação (HTTP 409).

---

### Autenticação — JWT + Argon2 + RBAC

Login com username, password e seleção de tipo de utilizador. Passwords hashed com Argon2id. Token JWT (30 min) no header `Authorization: Bearer`. **3 roles com permissões granulares:**

| Role | Permissões |
|------|-----------|
| Administrador | CRUD completo, gestão de utilizadores, ver todas as organizações |
| Gestor | Criar/editar clubes e mapas na sua organização |
| Cliente | Visualizar, ingressar em clubes |

<img width="1000" height="500" alt="Login" src="nuxt-app/assets/images/ManuelLogin.PNG" />

---

### Landing Page e About Us

Página inicial com hero section, call-to-action e barra de estatísticas em tempo real (total de clubes, utilizadores, mapas). Página "Sobre nós" com missão, valores e equipa.

---

### Notificações — Email SMTP + In-App

Sistema de notificações duplo: **emails HTML** enviados via SMTP com TLS (Gmail App Passwords) e **notificações persistentes** armazenadas em BD. O utilizador pode consultar o histórico de notificações via `GET /notificacoes`. Os emails são disparados automaticamente pelo Celery worker quando eventos de pagamento são processados.

---

## Quick Start

```bash
# 1. Clonar
git clone https://github.com/<user>/Manueli-s-Clubes.git
cd Manueli-s-Clubes

# 2. Configurar variáveis de ambiente
#    → .env (raiz): MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
#    → api/.env:   MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,
#                  MYSQL_DATABASE, SECRET_KEY, ALGORITHM,
#                  STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
#                  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM

# 3. Lançar tudo (5 containers: DB + Redis + API + Worker + Frontend)
docker compose up --build
```

| Serviço        | URL                          |
|----------------|------------------------------|
| Frontend       | http://localhost:3000         |
| API (Swagger)  | http://localhost:8000/docs    |
| PostgreSQL     | localhost:5432               |
| Redis          | localhost:6379               |

---

## Testes — 40/40 Passed

```bash
cd api && pytest tests/ -v --tb=short
```

```
tests/test_auth.py         ✅ 5 passed   (registo, login, token, password errada, rota protegida)
tests/test_clubes.py       ✅ 9 passed   (CRUD + inscrição + duplicação 409 + 404)
tests/test_utilizadores.py ✅ 5 passed   (list, update, delete, 404)
tests/test_tipouser.py     ✅ 7 passed   (CRUD + 404)
tests/test_mapas.py        ✅ 9 passed   (CRUD + clube inexistente + 404)
tests/test_stats.py        ✅ 5 passed   (stats, statstpuser, registrations, auth guard)
```

---

## Tech Stack

| Camada     | Tecnologia                         | Versão    |
|------------|------------------------------------|-----------| 
| Runtime    | Python                             | 3.11      |
| API        | FastAPI + Uvicorn                  | 0.115.6   |
| ORM        | SQLAlchemy                         | 2.0.36    |
| DB         | PostgreSQL (psycopg2)              | 15        |
| Cache      | Redis                              | 7         |
| Task Queue | Celery (broker + backend Redis)    | 5.4.0     |
| Auth       | python-jose (JWT) + Argon2         | —         |
| Pagamentos | Stripe API (Checkout + Webhooks)   | 8.4.0     |
| Email      | SMTP (TLS) via smtplib             | —         |
| Frontend   | Nuxt 3 (Vue 3, SSR)               | 3.x       |
| UI         | Bootstrap 5, SweetAlert2           | —         |
| Viz        | Chart.js, Leaflet.js, FullCalendar | —         |
| Container  | Docker + Docker Compose            | —         |

---

## Estrutura do Projeto

```
-Manueli-s-Clubes/
├── docker-compose.yml               # Orquestração: db + redis + api + worker + frontend
├── .env                             # Variáveis para Docker Compose (MYSQL_USER, etc.)
├── package.json                     # deps globais (Bootstrap, Chart.js, Leaflet)
│
├── api/                             # Backend (FastAPI + Celery)
│   ├── Dockerfile                   # python:3.11-slim → uvicorn :8000
│   ├── .env                         # Variáveis da API (DB, Stripe, SMTP, JWT)
│   ├── app/
│   │   ├── main.py                  # 34 endpoints: CRUD, stats, inscrições, pagamentos, webhooks, RBAC, cache
│   │   ├── auth.py                  # JWT + Argon2 + get_current_user + require_roles
│   │   ├── models.py                # 9 ORM models + 16 Pydantic schemas
│   │   ├── database.py              # PostgreSQL connection pool (SQLAlchemy)
│   │   ├── cache.py                 # Redis cache com TTL + invalidação por prefixo
│   │   ├── celery_app.py            # Configuração Celery (broker Redis)
│   │   ├── task.py                  # Tarefa assíncrona: processamento de webhooks Stripe
│   │   ├── email_service.py         # Envio de emails HTML via SMTP (TLS)
│   │   └── requirements.txt
│   └── tests/                       # 40 testes (pytest + httpx)
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_clubes.py
│       ├── test_mapas.py
│       ├── test_stats.py
│       ├── test_tipouser.py
│       └── test_utilizadores.py
│
└── nuxt-app/                        # Frontend (Nuxt 3)
    ├── Dockerfile                   # node:20 → :3000
    ├── pages/
    │   ├── index.vue                # Landing — stats públicas
    │   ├── login.vue                # Auth
    │   ├── dashboard.vue            # KPIs + Chart.js
    │   ├── clubes.vue               # CRUD table (scoped por organização)
    │   ├── mapas.vue                # Leaflet map
    │   ├── calendario.vue           # FullCalendar + inscrição
    │   ├── planos.vue               # Subscrições Stripe (Free/Pro/Enterprise)
    │   └── aboutus.vue              # Sobre nós
    └── components/
        ├── Header.vue               # Header global
        └── Navbar.vue               # Nav sidebar
```

---

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- DEEP DIVE — Secções técnicas em detalhes colapsáveis       -->
<!-- ═══════════════════════════════════════════════════════════ -->

<details>
<summary><strong>Arquitetura — Diagramas C4</strong></summary>

### Nível 1 — Contexto do Sistema

```mermaid
C4Context
    title System Context — Manueli's Clubes

    Person(user, "Utilizador", "Membro, Gestor ou Admin")
    System(sys, "Manueli's Clubes", "Plataforma SaaS de gestão de clubes")
    System_Ext(stripe, "Stripe", "Processamento de pagamentos + Webhooks")
    System_Ext(smtp, "Gmail SMTP", "Envio de emails transacionais")
    SystemDb(db, "PostgreSQL", "Armazenamento persistente")

    Rel(user, sys, "HTTPS / JSON")
    Rel(sys, db, "SQL via SQLAlchemy ORM")
    Rel(sys, stripe, "API REST (Checkout Sessions + Webhooks)")
    Rel(sys, smtp, "SMTP TLS :587")
    Rel(stripe, sys, "Webhooks HTTP POST")
```

### Nível 2 — Containers

```mermaid
C4Container
    title Container Diagram — Manueli's Clubes

    Person(user, "Utilizador")

    Container_Boundary(frontend, "Frontend") {
        Container(nuxt, "Nuxt 3 App", "Vue 3, SSR, Nitro", "SPA/SSR servida ao browser. Routing por ficheiro, Composition API.")
    }

    Container_Boundary(backend, "Backend") {
        Container(api, "FastAPI", "Python 3.11, Uvicorn", "API REST. Auth JWT, CRUD, inscrições, stats, pagamentos Stripe, webhooks. Cache Redis. RBAC com require_roles().")
        Container(worker, "Celery Worker", "Python 3.11, Celery 5.4", "Processamento assíncrono de webhooks Stripe. Retry com backoff exponencial. Envio de emails.")
        Container(auth_mod, "Auth Module", "python-jose, passlib[argon2]", "Registo, login, emissão/validação JWT.")
        Container(cache_mod, "Cache Module", "Redis 7", "Cache distribuído com TTL por key e invalidação por prefixo.")
        Container(email_mod, "Email Service", "smtplib, MIME", "Envio de emails HTML via SMTP TLS.")
    }

    System_Ext(stripe, "Stripe API", "Checkout Sessions + Subscriptions + Webhooks")
    System_Ext(smtp, "Gmail SMTP", "Email delivery")

    ContainerDb(db, "PostgreSQL", "psycopg2", "9 tabelas: clubes, utilizador, tipouser, mapas, membro_clube, planos, organizations, stripe_events, notificacoes")
    ContainerDb(redis, "Redis", "7-alpine", "Cache + Message Broker Celery")

    Rel(user, nuxt, "HTTPS :3000")
    Rel(nuxt, api, "fetch HTTP/JSON :8000", "Authorization: Bearer JWT")
    Rel(api, auth_mod, "Depends(get_current_user)")
    Rel(api, cache_mod, "cache_get / cache_set / cache_invalidate")
    Rel(api, stripe, "Stripe SDK")
    Rel(api, db, "SQLAlchemy Session")
    Rel(api, redis, "Enqueue tasks")
    Rel(worker, redis, "Consume tasks")
    Rel(worker, db, "SQLAlchemy Session")
    Rel(worker, email_mod, "payment_failed_email / payment_succeeded_email")
    Rel(email_mod, smtp, "SMTP TLS :587")
    Rel(stripe, api, "Webhooks POST /stripe/webhook")
    Rel(auth_mod, db, "SQLAlchemy Session")
    Rel(cache_mod, redis, "GET / SETEX / SCAN+DEL")
```

### Nível 3 — Componentes (API)

```mermaid
C4Component
    title Component Diagram — FastAPI Backend

    Container_Boundary(api, "FastAPI Application") {
        Component(main, "main.py", "FastAPI Router", "34 endpoints: CRUD clubes/utilizadores/tipouser/mapas/planos + stats + inscrições + Stripe checkout + webhooks + notificações. CORS middleware. RBAC require_roles(). Cache get/set nos GETs, invalidate nos writes. Startup init_db() + seed planos/tipos/org.")
        Component(auth, "auth.py", "APIRouter /auth", "POST /auth/ (register), POST /auth/token (login). Argon2 hash/verify. JWT encode/decode. get_current_user dependency.")
        Component(models, "models.py", "SQLAlchemy + Pydantic", "9 ORM models (incl. StripeEventModel, NotificacaoModel) + relationships + cascade config. 16 Pydantic schemas para request/response validation.")
        Component(database, "database.py", "Engine + SessionLocal", "Connection string via env vars. get_db() generator. init_db() → Base.metadata.create_all().")
        Component(cache, "cache.py", "Redis client", "cache_get(key), cache_set(key, value, ttl), cache_invalidate(*prefixes). TTL via Redis SETEX.")
        Component(celery_app, "celery_app.py", "Celery config", "Broker + backend Redis. JSON serializer. include=['app.task'].")
        Component(task, "task.py", "Celery Task", "process_stripe_event: idempotência, retry com backoff, atualização de plano, notificações, email.")
        Component(email, "email_service.py", "SMTP client", "send_email(), payment_failed_email(), payment_succeeded_email(). STARTTLS + login.")
    }

    ContainerDb(db, "PostgreSQL")
    ContainerDb(redis, "Redis")
    System_Ext(stripe, "Stripe API")

    Rel(main, auth, "include_router(auth.router)")
    Rel(main, models, "importa Models + Schemas")
    Rel(main, database, "Depends(get_db)")
    Rel(main, cache, "cache_get / cache_set / cache_invalidate")
    Rel(main, stripe, "stripe.checkout.Session.create()")
    Rel(main, task, "process_stripe_event.delay()")
    Rel(task, models, "StripeEventModel, UtilizadorModel, PlanoModel, NotificacaoModel")
    Rel(task, email, "payment_failed_email / payment_succeeded_email")
    Rel(task, cache, "cache_invalidate")
    Rel(auth, models, "importa UtilizadorModel")
    Rel(auth, database, "SessionLocal()")
    Rel(database, db, "psycopg2 connection pool")
    Rel(cache, redis, "redis-py client")
    Rel(celery_app, redis, "broker + backend")
```

</details>

<details>
<summary><strong>Modelo de Dados (ER)</strong></summary>

```mermaid
erDiagram
    organizations ||--o{ utilizador : "1:N"
    organizations ||--o{ clubes : "1:N"
    tipouser ||--o{ utilizador : "1:N"
    planos ||--o{ utilizador : "1:N"
    utilizador ||--o{ membro_clube : "1:N"
    utilizador ||--o{ notificacoes : "1:N"
    clubes ||--o{ membro_clube : "1:N"
    clubes ||--o{ mapas : "1:N"

    organizations {
        int id PK
        varchar(100) nome
        datetime created_at
    }

    planos {
        int id PK
        varchar(100) nome
        float preco
        int limite_clubes
        int limite_mapas
        datetime created_at
    }

    tipouser {
        int id PK
        varchar(100) descricao
    }

    utilizador {
        int id PK
        varchar(50) username UK
        varchar(255) email
        varchar(255) password
        datetime created_at
        int tipo_id FK
        int plano_id FK
        int organization_id FK
    }

    clubes {
        int id PK
        varchar(100) nome
        varchar(150) email UK
        varchar(20) telefone
        varchar(100) localidade
        date evento_at
        datetime created_at
        int organization_id FK
    }

    membro_clube {
        int id PK
        int utilizador_id FK
        int clube_id FK
        datetime inscrito_em
    }

    mapas {
        int id PK
        varchar(255) descricao
        float latitude
        float longitude
        int clube_id FK
    }

    stripe_events {
        int id PK
        varchar(255) event_id UK
        varchar(100) event_type
        datetime processed_at
    }

    notificacoes {
        int id PK
        int utilizador_id FK
        varchar(50) tipo
        varchar(200) titulo
        text mensagem
        boolean lida
        datetime created_at
    }
```

> **Constraints:** `UniqueConstraint("utilizador_id", "clube_id")` em `membro_clube` — impede inscrição duplicada a nível de BD. `unique=True` em `utilizador.username`, `clubes.email` e `stripe_events.event_id` (idempotência de webhooks).

</details>

<details>
<summary><strong>Cache — Redis com TTL e Invalidação por Prefixo</strong></summary>

O sistema usa **Redis** como backend de cache (`cache.py`) com TTL por key e invalidação automática por prefixo em operações de escrita. O mesmo Redis serve também de broker e backend para o Celery.

### Módulo `cache.py`

```python
import os
import json
from typing import Any
import redis

_redis = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)

def cache_get(key: str) -> Any | None:
    value = _redis.get(key)
    if value is None:
        return None
    return json.loads(value)

def cache_set(key: str, value: Any, ttl: int) -> None:
    _redis.setex(key, ttl, json.dumps(value, default=str))

def cache_invalidate(*prefixes: str) -> None:
    for prefix in prefixes:
        for key in _redis.scan_iter(f"{prefix}*"):
            _redis.delete(key)
```

### Tabela de TTL e Invalidação

| Endpoint GET          | Cache Key              | TTL    | Invalidado por                           |
|-----------------------|------------------------|--------|------------------------------------------|
| `GET /stats`          | `stats`                | 60 s   | POST/PUT/DELETE clubes, utilizadores, mapas, tipouser |
| `GET /statstpuser`    | `statstpuser`          | 60 s   | POST/PUT/DELETE utilizadores, tipouser   |
| `GET /registrations`  | `registrations:{year}` | 300 s  | DELETE/PUT utilizadores                  |
| `GET /clubes`         | `clubes:org:{id}:list` | 30 s   | POST/PUT/DELETE clubes                   |
| `GET /clubesAdmin`    | `clubes:admin:list`    | 30 s   | POST/PUT/DELETE clubes                   |
| `GET /tipouser`       | `tipouser:list`        | 120 s  | POST/PUT/DELETE tipouser                 |
| `GET /mapas`          | `mapas:list`           | 60 s   | POST/PUT/DELETE mapas                    |
| `GET /planos`         | `planos:list`          | 120 s  | POST/PUT/DELETE planos                   |
| `GET /utilizadores`   | `utilizadores:list`    | 30 s   | PUT /me/plano, DELETE utilizadores       |

</details>

<details>
<summary><strong>Endpoints da API</strong></summary>

### Auth (`/auth`)

| Método | Rota           | Body / Params                              | Response          | Auth |
|--------|----------------|--------------------------------------------|-------------------|------|
| POST   | `/auth/`       | `{username, password, tipo_id}`            | `201` message     | —    |
| POST   | `/auth/token`  | FormData: `username, password, tipo_id`    | `{access_token, token_type}` | — |

### Perfil (`/me`)

| Método | Rota              | Body / Params | Response            | Auth | Status Codes |
|--------|--------------------|---------------|---------------------|------|--------------|
| GET    | `/me`              | —             | `UtilizadorResponse`| JWT  | 200          |
| PUT    | `/me/plano/{id}`   | —             | `UtilizadorResponse`| JWT  | 200, 404     |

### Clubes (`/clubes`)

| Método | Rota                     | Body / Params       | Response            | Auth         | Status Codes     | Cache                              |
|--------|--------------------------|---------------------|---------------------|--------------|------------------|-------------------------------------|
| POST   | `/clubes`                | `ClubeCreate`       | `ClubeResponse`     | Admin/Gestor | 201, 403, 409    | invalidate `stats`, `clubes:`       |
| GET    | `/clubes`                | —                   | `[ClubeResponse]`   | JWT          | 200              | `clubes:org:{id}:list` TTL 30 s     |
| GET    | `/clubesAdmin`           | —                   | `[ClubeResponse]`   | Admin        | 200              | `clubes:admin:list` TTL 30 s        |
| PUT    | `/clubes/{id}`           | `ClubeCreate`       | `ClubeResponse`     | Admin/Gestor | 200, 404         | invalidate `stats`, `clubes:`       |
| DELETE | `/clubes/{id}`           | —                   | —                   | Admin        | 204, 404         | invalidate `stats`, `clubes:`       |
| POST   | `/clubes/{id}/ingressar` | —                   | `IngressarResponse` | JWT          | 201, 404, 409    | —                                   |

### Utilizadores (`/utilizadores`)

| Método | Rota                  | Body / Params       | Response               | Auth  | Status Codes | Cache                                        |
|--------|-----------------------|---------------------|------------------------|-------|--------------|----------------------------------------------|
| GET    | `/utilizadores`       | —                   | `[UtilizadorResponse]` | Admin | 200          | `utilizadores:list` TTL 30 s                 |
| PUT    | `/utilizadores/{id}`  | `UtilizadorCreate`  | `UtilizadorResponse`   | Admin | 200, 404     | invalidate `stats`, `statstpuser`            |
| DELETE | `/utilizadores/{id}`  | —                   | —                      | Admin | 204, 404     | invalidate `stats`, `statstpuser`, `registrations:` |

### Tipos de Utilizador (`/tipouser`)

| Método | Rota              | Body / Params    | Response             | Auth | Status Codes | Cache                                         |
|--------|--------------------|------------------|----------------------|------|--------------|-----------------------------------------------|
| POST   | `/tipouser`        | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200          | invalidate `stats`, `statstpuser`, `tipouser:` |
| GET    | `/tipouser`        | —                | `[TipoUserResponse]` | —    | 200          | `tipouser:list` TTL 120 s                     |
| PUT    | `/tipouser/{id}`   | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200, 404     | invalidate `stats`, `statstpuser`, `tipouser:` |
| DELETE | `/tipouser/{id}`   | —                | —                    | JWT  | 204, 404     | invalidate `stats`, `statstpuser`, `tipouser:` |

### Mapas (`/mapas`)

| Método | Rota           | Body / Params | Response          | Auth         | Status Codes | Cache                          |
|--------|----------------|---------------|-------------------|--------------|--------------|--------------------------------|
| POST   | `/mapas`       | `MapaCreate`  | `MapaResponse`    | Admin/Gestor | 200, 404     | invalidate `stats`, `mapas:`   |
| GET    | `/mapas`       | —             | `[MapaResponse]`  | JWT          | 200          | `mapas:list` TTL 60 s          |
| PUT    | `/mapas/{id}`  | `MapaCreate`  | `MapaResponse`    | Admin/Gestor | 200, 404     | invalidate `stats`, `mapas:`   |
| DELETE | `/mapas/{id}`  | —             | message           | Admin/Gestor | 200, 404     | invalidate `stats`, `mapas:`   |

### Planos (`/planos`)

| Método | Rota           | Body / Params | Response           | Auth | Status Codes | Cache                  |
|--------|----------------|---------------|--------------------|------|--------------|------------------------|
| GET    | `/planos`      | —             | `[PlanoResponse]`  | —    | 200          | `planos:list` TTL 120 s|
| POST   | `/planos`      | `PlanoCreate` | `PlanoResponse`    | JWT  | 201          | invalidate `planos:`   |
| PUT    | `/planos/{id}` | `PlanoCreate` | `PlanoResponse`    | JWT  | 200, 404     | invalidate `planos:`   |
| DELETE | `/planos/{id}` | —             | —                  | JWT  | 204, 404     | invalidate `planos:`   |

### Organizations (`/organizations`)

| Método | Rota              | Body / Params | Response  | Auth  | Status Codes |
|--------|--------------------|---------------|-----------|-------|--------------|
| POST   | `/organizations`   | `nome`        | Org data  | Admin | 201          |
| GET    | `/organizations`   | —             | `[Org]`   | Admin | 200          |

### Pagamentos e Webhooks (Stripe)

| Método | Rota                       | Body / Params    | Response     | Auth | Status Codes       |
|--------|----------------------------|------------------|--------------|------|--------------------|
| POST   | `/create-checkout-session` | `{plano_id}`     | `{url}`      | JWT  | 200, 400, 404, 502 |
| POST   | `/stripe/webhook`          | Stripe payload   | `{status}`   | —    | 200, 400           |

### Notificações (`/notificacoes`)

| Método | Rota            | Body / Params | Response                | Auth | Status Codes |
|--------|-----------------|---------------|-------------------------|------|--------------|
| GET    | `/notificacoes` | —             | `[NotificacaoResponse]` | JWT  | 200          |

### Estatísticas

| Método | Rota             | Response                                        | Auth | Cache                          |
|--------|-------------------|-------------------------------------------------|------|--------------------------------|
| GET    | `/stats`          | `{clubes, utilizadores, tipousers, mapas}`      | —    | `stats` TTL 60 s               |
| GET    | `/statstpuser`    | `{tipo_descricao: count, ...}`                  | JWT  | `statstpuser` TTL 60 s         |
| GET    | `/registrations`  | `[{month: str, count: int}]` (12 meses)        | JWT  | `registrations:{year}` TTL 300 s |

</details>

<details>
<summary><strong>Pydantic Schemas (Contratos)</strong></summary>

```python
# ──── Request ────
class ClubeCreate(BaseModel):
    nome: str
    email: str | None = None
    telefone: str | None = None
    localidade: str | None = None
    evento_at: Optional[date] = None

class UtilizadorCreate(BaseModel):
    username: str
    password: str
    tipo_id: int

class TipoUserCreate(BaseModel):
    descricao: str

class MapaCreate(BaseModel):
    descricao: str | None = None
    latitude: float
    longitude: float
    clube_id: int

class PlanoCreate(BaseModel):         
    nome: str
    preco: float = 0.0
    limite_clubes: int = -1
    limite_mapas: int = -1

class CheckoutRequest(BaseModel):     
    plano_id: int

# ──── Response ────
class ClubeResponse(ClubeCreate):
    id: int
    organization_id: int              # multi-tenancy

class UtilizadorResponse(BaseModel):
    id: int
    username: str
    tipo: TipoUserResponse
    plano: PlanoResponse | None      
    organization: OrganizationResponse | None  
    created_at: datetime

class PlanoResponse(BaseModel):      
    id: int
    nome: str | None
    preco: float
    limite_clubes: int
    limite_mapas: int

class OrganizationResponse(BaseModel): 
    id: int
    nome: str
    created_at: datetime | None

class MapaResponse(BaseModel):
    id: int
    descricao: str | None = None
    latitude: float
    longitude: float
    clube_id: int

class IngressarResponse(BaseModel):
    mensagem:    str
    clube_id:    int
    clube_nome:  str
    inscrito_em: datetime

class NotificacaoResponse(BaseModel):
    id:         int
    tipo:       str
    titulo:     str
    mensagem:   str
    lida:       bool
    created_at: datetime
```

</details>

<details>
<summary><strong>Sequence Diagrams</strong></summary>

### Autenticação (Login + Acesso Protegido)

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant F as Nuxt Frontend
    participant A as FastAPI /auth
    participant DB as PostgreSQL

    U->>F: Preenche username, password, tipo_id
    F->>A: POST /auth/token (FormData)
    A->>DB: SELECT utilizador WHERE username = ?
    DB-->>A: row | null

    alt Utilizador não existe
        A-->>F: 401 Unauthorized
    else Password inválida (Argon2 verify fail)
        A-->>F: 401 Unauthorized
    else tipo_id não corresponde
        A-->>F: 401 Unauthorized
    else Credenciais válidas
        A->>A: jwt.encode({sub, id, tipo_id, exp+30min}, SECRET_KEY, HS256)
        A-->>F: 200 {access_token, token_type: bearer}
    end

    F->>F: Armazena token + navigateTo("/dashboard")
```

### Stripe Checkout — Subscrição de Plano

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant P as Nuxt (planos.vue)
    participant API as FastAPI
    participant S as Stripe API
    participant DB as PostgreSQL

    U->>P: Clica "Escolher Pro"
    P->>API: POST /create-checkout-session {plano_id: 2} + Bearer JWT
    API->>DB: SELECT plano WHERE id = 2
    DB-->>API: {nome: "Pro", preco: 9.99}
    API->>S: stripe.checkout.Session.create(mode=subscription)
    S-->>API: {url: "https://checkout.stripe.com/..."}
    API-->>P: {url}
    P->>P: window.location.href = url

    Note over U,S: Utilizador completa pagamento no Stripe

    S-->>P: Redirect → /planos?success=true&plano_id=2
    P->>API: PUT /me/plano/2 + Bearer JWT
    API->>DB: UPDATE utilizador SET plano_id = 2
    DB-->>API: ✓
    API-->>P: UtilizadorResponse (plano atualizado)
    P->>P: "Plano Pro ativado com sucesso!"
```

### Stripe Webhook — Processamento Assíncrono de Eventos

```mermaid
sequenceDiagram
    participant S as Stripe
    participant API as FastAPI
    participant R as Redis (Broker)
    participant W as Celery Worker
    participant DB as PostgreSQL
    participant SMTP as Gmail SMTP

    S->>API: POST /stripe/webhook (assinatura HMAC)
    API->>API: stripe.Webhook.construct_event() — validação
    API->>DB: Verifica duplicado (event_id)
    API->>R: process_stripe_event.delay(event_id, type, data)
    API-->>S: 200 {status: "queued"}

    R->>W: Entrega tarefa

    alt invoice.payment_failed
        W->>DB: SELECT utilizador WHERE email = customer_email
        W->>DB: UPDATE plano_id → Free
        W->>DB: INSERT notificacao (payment_failed)
        W->>DB: INSERT stripe_event (idempotência)
        W->>SMTP: payment_failed_email (HTML)
        W->>R: cache_invalidate("utilizadores:", "planos:")
    else invoice.payment_succeeded
        W->>DB: INSERT notificacao (payment_succeeded)
        W->>DB: INSERT stripe_event
        W->>SMTP: payment_succeeded_email (HTML)
    else checkout.session.completed
        W->>DB: UPDATE utilizador SET plano_id
        W->>DB: INSERT stripe_event
        W->>R: cache_invalidate("utilizadores:", "planos:")
    end

    Note over W: Retry automático com backoff exponencial (max 5 tentativas)
```

### CRUD — Criar Clube (com RBAC + limites de plano)

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant F as Nuxt (clubes.vue)
    participant API as FastAPI
    participant C as Cache (dict)
    participant DB as PostgreSQL

    U->>F: Preenche formulário (nome, email, tel, localidade, evento_at)
    F->>API: POST /clubes {ClubeCreate} + Bearer JWT
    API->>API: require_roles("Administrador", "Gestor")

    alt Role não autorizada
        API-->>F: 403 "Sem permissão"
    else Role válida
        API->>DB: SELECT COUNT(*) FROM clubes WHERE organization_id = ?
        alt Limite do plano atingido
            API-->>F: 403 "Limite de X clube(s) atingido"
        else Dentro do limite
            API->>DB: INSERT INTO clubes VALUES(...)
            DB-->>API: clube row
            API->>C: cache_invalidate("stats", "clubes:")
            API-->>F: 201 ClubeResponse {id, nome, ...}
            F->>F: Swal.fire("Sucesso")
        end
    end
```

### Inscrição em Clube (via Calendário)

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant C as Nuxt (calendario.vue)
    participant API as FastAPI
    participant DB as PostgreSQL

    U->>C: Clica evento no FullCalendar
    C->>C: Abre modal (nome, email, tel, localidade)
    U->>C: Clica "Ingressar"
    C->>API: POST /clubes/{id}/ingressar + Bearer JWT

    API->>API: Depends(get_current_user) → extrai user.id
    API->>DB: SELECT clube WHERE id = ?
    
    alt Clube não encontrado
        API-->>C: 404 "Clube não encontrado"
    else Clube existe
        API->>DB: INSERT INTO membro_clube (utilizador_id, clube_id)
        
        alt IntegrityError (UQ violation)
            DB-->>API: IntegrityError
            API->>API: db.rollback()
            API-->>C: 409 "Já está inscrito no clube 'X'"
        else Sucesso
            DB-->>API: row
            API-->>C: 201 IngressarResponse {mensagem, clube_id, clube_nome, inscrito_em}
        end
    end

    C->>C: Swal.fire(response.mensagem)
```

### Dashboard — Carregamento de Estatísticas (com cache Redis)

```mermaid
sequenceDiagram
    participant F as Nuxt (dashboard.vue)
    participant API as FastAPI
    participant C as Redis (Cache)
    participant DB as PostgreSQL

    F->>API: GET /stats
    API->>C: cache_get("stats")
    alt Cache hit
        C-->>API: {clubes, utilizadores, tipousers, mapas}
        API-->>F: 200 (from cache)
    else Cache miss
        C-->>API: None
        API->>DB: SELECT COUNT(*) FROM clubes, utilizador, tipouser, mapas
        DB-->>API: {counts}
        API->>C: cache_set("stats", result, ttl=60)
        API-->>F: 200 {clubes, utilizadores, tipousers, mapas}
    end

    par Parallel requests
        F->>API: GET /statstpuser (Authorization: Bearer token)
        API->>C: cache_get("statstpuser")
        alt Cache hit
            C-->>API: {tipo: count}
        else Cache miss
            API->>DB: GROUP BY tipo_id, COUNT(*)
            DB-->>API: {tipo: count}
            API->>C: cache_set("statstpuser", result, ttl=60)
        end
        API-->>F: {admin: N, gestor: N, ...}
    and
        F->>API: GET /registrations (Authorization: Bearer token)
        API->>C: cache_get("registrations:2026")
        alt Cache hit
            C-->>API: [{month, count}]
        else Cache miss
            API->>DB: SELECT EXTRACT(month), COUNT(*) WHERE year = current GROUP BY month
            DB-->>API: [{month, count}]
            API->>C: cache_set("registrations:2026", data, ttl=300)
        end
        API-->>F: [{month: "Janeiro", count: N}, ...]
    end

    F->>F: Chart.js render (line + doughnut)
```

</details>

<details>
<summary><strong>Testes — Código Completo</strong></summary>

### Estrutura

```
api/tests/
├── conftest.py          # Fixtures: TestClient, BD em memória, token helper
├── test_auth.py         # Registo, login, token inválido
├── test_clubes.py       # CRUD clubes + inscrição + duplicação
├── test_utilizadores.py # CRUD utilizadores
├── test_tipouser.py     # CRUD tipos
├── test_mapas.py        # CRUD mapas
└── test_stats.py        # Endpoints de estatísticas
```

### `conftest.py`

```python
import os
os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "5432")
os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test_db")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
import auth, database

database.init_db = lambda: None

from main import app
from models import TipoUserModel

import main as _main_module
_main_module.init_db = lambda: None

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[auth.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def _seed_tipo(db, descricao="admin"):
    tipo = TipoUserModel(descricao=descricao)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo

@pytest.fixture()
def tipo(db):
    return _seed_tipo(db)

@pytest.fixture()
def auth_headers(client, db):
    tipo = _seed_tipo(db)
    client.post("/auth/", json={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": tipo.id})
    resp = client.post("/auth/token", data={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": str(tipo.id)})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### `test_auth.py`

```python
from tests.conftest import _seed_tipo

def test_register_success(client, db):
    _seed_tipo(db)
    resp = client.post("/auth/", json={"username": "newuser", "password": "Str0ng!Pass", "tipo_id": 1})
    assert resp.status_code == 201

def test_register_duplicate_username(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={"username": "dup", "password": "Pass1!abc", "tipo_id": 1})
    resp = client.post("/auth/", json={"username": "dup", "password": "Pass2!abc", "tipo_id": 1})
    assert resp.status_code == 400

def test_login_returns_jwt(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": 1})
    resp = client.post("/auth/token", data={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": "1"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_login_wrong_password(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": 1})
    resp = client.post("/auth/token", data={"username": "testuser", "password": "wrong", "tipo_id": "1"})
    assert resp.status_code == 401

def test_protected_route_without_token(client):
    resp = client.get("/clubes")
    assert resp.status_code == 401
```

### `test_clubes.py`

```python
def test_create_clube(client, auth_headers):
    resp = client.post("/clubes", json={"nome": "Clube Teste", "email": "teste@clube.pt", "telefone": "912345678", "localidade": "Lisboa", "evento_at": "2026-06-15"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Clube Teste"

def test_list_clubes(client, auth_headers):
    client.post("/clubes", json={"nome": "C1"}, headers=auth_headers)
    client.post("/clubes", json={"nome": "C2"}, headers=auth_headers)
    resp = client.get("/clubes", headers=auth_headers)
    assert len(resp.json()) == 2

def test_update_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Old"}, headers=auth_headers)
    resp = client.put(f"/clubes/{create.json()['id']}", json={"nome": "New"}, headers=auth_headers)
    assert resp.json()["nome"] == "New"

def test_delete_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "ToDelete"}, headers=auth_headers)
    resp = client.delete(f"/clubes/{create.json()['id']}", headers=auth_headers)
    assert resp.status_code == 204

def test_delete_clube_404(client, auth_headers):
    assert client.delete("/clubes/9999", headers=auth_headers).status_code == 404

def test_ingressar_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Ingresso"}, headers=auth_headers)
    resp = client.post(f"/clubes/{create.json()['id']}/ingressar", headers=auth_headers)
    assert resp.status_code == 201

def test_ingressar_duplicate_409(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Dup"}, headers=auth_headers)
    cid = create.json()["id"]
    client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    assert client.post(f"/clubes/{cid}/ingressar", headers=auth_headers).status_code == 409

def test_ingressar_clube_inexistente_404(client, auth_headers):
    assert client.post("/clubes/9999/ingressar", headers=auth_headers).status_code == 404
```

### Cobertura

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

| Módulo            | Cobertura Alvo |
|-------------------|----------------|
| `auth.py`         | ≥ 90%          |
| `main.py`         | ≥ 85%          |
| `models.py`       | ≥ 95%          |
| `database.py`     | ≥ 80%          |
| `cache.py`        | ≥ 90%          |
| `task.py`         | ≥ 80%          |
| `email_service.py`| ≥ 75%          |

</details>

<details>
<summary><strong>Architecture Decision Records (ADR)</strong></summary>

### ADR-001: FastAPI em vez de Django REST / Flask

**Status:** Aceite  
**Decisão:** FastAPI com Pydantic + SQLAlchemy — documentação OpenAPI automática, validação nativa, DI com `Depends()`, performance ASGI.

### ADR-002: Argon2 em vez de bcrypt

**Status:** Aceite  
**Decisão:** Argon2id via `passlib[argon2]` — vencedor da Password Hashing Competition, resistente a GPU/ASIC, parâmetros configuráveis.

### ADR-003: JWT via Bearer token

**Status:** Aceite  
**Decisão:** JWT no header `Authorization: Bearer <token>`. Login devolve `{access_token, token_type}`, frontend gere armazenamento. Stateless, compatível com `OAuth2PasswordBearer` do FastAPI.

### ADR-004: UniqueConstraint em membro_clube

**Status:** Aceite  
**Decisão:** `UniqueConstraint("utilizador_id", "clube_id")` a nível de BD + catch `IntegrityError` → HTTP 409. Impossível bypass via SQL direto ou race conditions.

### ADR-005: SSR (Nuxt) com `<ClientOnly>`

**Status:** Aceite  
**Decisão:** SSR por default para SEO. FullCalendar e Leaflet renderizados apenas client-side via `<ClientOnly>` com skeleton fallback.

### ADR-006: CORS wildcard em dev

**Status:** Aceite  
**Decisão:** `allow_origins=["*"]` com `allow_credentials=False` em dev (Bearer tokens não precisam de cookies). Em produção, restringir ao domínio real.

### ADR-007: Monólito modular

**Status:** Aceite  
**Decisão:** Monorepo com módulos separados (`main.py`, `auth.py`, `models.py`, `database.py`, `cache.py`). Deploy simples, sem overhead de microserviços.

### ADR-008: Redis como cache e message broker

**Status:** Aceite  
**Decisão:** Redis 7 serve dupla função: cache com TTL via `SETEX` + invalidação por `SCAN`/`DEL` por prefixo, e message broker + result backend do Celery. Uma única instância Redis simplifica a infraestrutura, elimina estado em memória do processo API e permite escalamento horizontal de workers.

### ADR-009: Stripe Checkout para pagamentos

**Status:** Aceite  
**Decisão:** Stripe Checkout Sessions com modo `subscription` para planos recorrentes. Evita complexidade de PCI compliance — toda a UI de pagamento é hosted pelo Stripe. Redirect-based flow com `success_url` e `cancel_url` que inclui `plano_id`.

### ADR-010: Multi-tenancy por organização

**Status:** Aceite  
**Decisão:** Cada utilizador pertence a uma `organization`. Clubes são scoped à organização do utilizador (`ClubeModel.organization_id`). Admins podem ver todos via `/clubesAdmin`. Isolamento via query filter `WHERE organization_id = user.organization_id`.

### ADR-011: RBAC com require_roles()

**Status:** Aceite  
**Decisão:** Middleware `require_roles(*roles)` como FastAPI Dependency. 3 roles: Administrador (CRUD total), Gestor (criar/editar), Cliente (leitura). Enforcement a nível de endpoint, não de frontend.

### ADR-012: Celery para processamento assíncrono de webhooks

**Status:** Aceite  
**Decisão:** Stripe webhooks são recebidos pela API e despachados para um Celery worker via Redis. Permite resposta imediata ao Stripe (< 200 ms), retry automático com backoff exponencial (max 5 tentativas) e idempotência via tabela `stripe_events`.

### ADR-013: Notificações por email via SMTP

**Status:** Aceite  
**Decisão:** Emails transacionais (pagamento falhado/sucedido) via `smtplib` com STARTTLS no Gmail (porta 587). Processados no worker Celery para não bloquear a API. Templates HTML inline com formatação responsiva.

</details>

<details>
<summary><strong>Docker — Configuração Completa</strong></summary>

### Serviços

| Serviço    | Imagem Base        | Container          | Porta  | Descrição                              |
|------------|--------------------|--------------------|--------|----------------------------------------|
| `db`       | `postgres:15`      | `clubes_db`        | 5432   | PostgreSQL com volume persistente + healthcheck |
| `redis`    | `redis:7-alpine`   | `clubes_redis`     | 6379   | Cache + Celery broker/backend          |
| `api`      | `python:3.11-slim` | `clubes_api`       | 8000   | FastAPI + Uvicorn                      |
| `worker`   | `python:3.11-slim` | `clubes_worker`    | —      | Celery worker (webhooks + emails)      |
| `frontend` | `node:20`          | `clubes_frontend`  | 3000   | Nuxt 3 SSR                             |

### `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:15
    container_name: clubes_db
    restart: always
    environment:
      POSTGRES_USER: ${MYSQL_USER}
      POSTGRES_PASSWORD: ${MYSQL_PASSWORD}
      POSTGRES_DB: ${MYSQL_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - clubes_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: clubes_redis
    restart: always
    ports:
      - "6379:6379"
    networks:
      - clubes_net

  api:
    build: ./api
    container_name: clubes_api
    ports:
      - "8000:8000"
    env_file:
      - ./api/.env
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - clubes_net

  worker:
    build: ./api
    container_name: clubes_worker
    command: celery -A app.celery_app:celery worker --loglevel=info
    env_file:
      - ./api/.env
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - clubes_net

  frontend:
    build: ./nuxt-app
    container_name: clubes_frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
    networks:
      - clubes_net

volumes:
  postgres_data:

networks:
  clubes_net:
    driver: bridge
```

### Dockerfiles

**API** (`api/Dockerfile`):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/ .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend** (`nuxt-app/Dockerfile`):
```dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "dev"]
```

### Diagrama de Rede

```mermaid
graph LR
    subgraph clubes_net [Docker Network — clubes_net]
        DB["clubes_db<br/>postgres:15<br/>:5432"]
        RD["clubes_redis<br/>redis:7-alpine<br/>:6379"]
        API["clubes_api<br/>python:3.11-slim<br/>:8000"]
        WK["clubes_worker<br/>python:3.11-slim<br/>Celery"]
        FE["clubes_frontend<br/>node:20<br/>:3000"]
    end

    FE -->|depends_on| API
    API -->|service_healthy| DB
    API -->|service_started| RD
    WK -->|service_healthy| DB
    WK -->|broker + backend| RD
    API -->|task.delay()| RD
    Browser([Browser]) -->|:3000| FE
    Browser -->|:8000| API
```

</details>

<details>
<summary><strong>Setup Local (sem Docker)</strong></summary>

### Variáveis de Ambiente

**`api/.env`** — Backend:
```env
MYSQL_HOST=localhost
MYSQL_PORT=5432
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_DATABASE=federacao
SECRET_KEY=<random-256-bit-hex>
ALGORITHM=HS256
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<gmail>
SMTP_PASSWORD=<app-password>
SMTP_FROM=<gmail>
FRONTEND_URL=http://localhost:3000
REDIS_URL=redis://localhost:6379/0
```

**`.env`** (raiz) — Docker Compose:
```env
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_DB=federacao
SECRET_KEY=<random-256-bit-hex>
ALGORITHM=HS256
```

### Backend

```bash
cd api/app
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
# → http://localhost:8000/docs (Swagger UI)
```

### Frontend

```bash
cd nuxt-app
npm install
npm run dev
# → http://localhost:3000
```

</details>

---

## Autor

**Manuel Silvestre**
