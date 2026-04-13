<div align="center">

# Manueli's Clubes

**Plataforma SaaS de gestão de clubes** — pagamentos Stripe reais, webhooks assíncronos, multi-tenancy e RBAC

<img width="1000" height="500" alt="ManueliClube" src="https://github.com/user-attachments/assets/786aee57-cdbc-4be2-823b-51c221d7e4b8" />

<p>
  <a href="https://github.com/Wand-DenaXy/-Manueli-s-Clubes/actions"><img alt="CI" src="https://github.com/Wand-DenaXy/-Manueli-s-Clubes/actions/workflows/ci.yml/badge.svg" /></a>
  <img alt="Coverage" src="https://img.shields.io/badge/coverage-93%25-brightgreen?logo=pytest&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" />
  <img alt="Nuxt" src="https://img.shields.io/badge/Nuxt-3-00DC82?logo=nuxtdotjs&logoColor=white" />
  <img alt="Stripe" src="https://img.shields.io/badge/Stripe-Checkout%20+%20Webhooks-635BFF?logo=stripe&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" />
</p>

</div>

---

**34** endpoints REST · **72** testes · **93%** coverage · **9** modelos ORM · **5** Docker containers · **3** roles RBAC

---

## Porquê este projeto?

Queria construir algo que **funcionasse como um produto real**, não mais um CRUD académico. Clubes desportivos lidam com membros, eventos, mapas e pagamentos — complexo o suficiente para justificar multi-tenancy, RBAC, subscrições recorrentes e webhooks assíncronos. O objetivo: levar uma ideia de zero a produção com stack e práticas de empresa.

---

## O que o torna interessante

- **Stripe Checkout reais** — subscrições recorrentes (Free €0 · Pro €9.99 · Enterprise €29.99), não mocks
- **Webhooks assíncronos** — Celery com retry (backoff exponencial, max 5), idempotência por `event_id`
- **Emails transacionais** — confirmação de pagamento ou aviso de falha + rollback automático para Free
- **Multi-tenancy + RBAC** — isolamento por organização, 3 roles server-side (`require_roles()`)
- **Redis** — cache com TTL + invalidação por prefixo + broker Celery, numa instância
- **CI com 3 gates** — testes + coverage ≥ 75%, lint (ruff), Docker build — falha = bloqueia merge

---

## Planos

Limites enforced server-side. Falha de pagamento → plano revertido para Free + email.

| | Free | Pro | Enterprise |
|---|---|---|---|
| **Preço** | €0 | €9.99/mês | €29.99/mês |
| **Clubes** | 3 | 15 | ∞ |
| **Mapas** | 1 | 20 | ∞ |
| **Checkout** | — | Stripe → webhook → email | Stripe → webhook → email |

---

## Arquitetura

```mermaid
graph LR
    Browser -->|:3000| Nuxt[Nuxt 3 SSR]
    Nuxt -->|JWT| API[FastAPI :8000]
    API --> DB[(PostgreSQL)]
    API --> Redis[(Redis)]
    Stripe -->|Webhooks| API
    API -->|.delay| Worker[Celery Worker]
    Worker --> DB
    Worker --> Redis
    Worker -->|SMTP TLS| Email[Gmail]
```

---

## Stack

| Backend | Frontend | Infra |
|---------|----------|-------|
| Python 3.11 · FastAPI · SQLAlchemy | Nuxt 3 · Vue 3 · Bootstrap 5 | PostgreSQL 15 · Redis 7 |
| Celery 5.4 · Stripe 8.4 | Chart.js · Leaflet · FullCalendar | Docker Compose · GitHub Actions |
| JWT (HS256) · Argon2id · SMTP | SweetAlert2 | ruff · pytest-cov |

---

## Qualidade

[![CI](https://github.com/Wand-DenaXy/-Manueli-s-Clubes/actions/workflows/ci.yml/badge.svg)](https://github.com/Wand-DenaXy/-Manueli-s-Clubes/actions)

```
72 tests · 93% coverage · lint clean · Docker OK
```

**Edge cases testados:** JWT forjado → 401 · limite plano → 403 · inscrição duplicada → 409 · webhook inválido → 400 · evento duplicado → idempotência · Stripe API error → 502 · SMTP off → no-op

<details>
<summary>Breakdown por ficheiro</summary>

```
test_auth.py          7    register, JWT, wrong password, tampered token
test_clubes.py        9    CRUD, ingressar, duplicate 409, plan limit 403
test_email.py         5    SMTP config, send ok/fail, payment emails
test_endpoints.py    14    /me, /clubesAdmin, /organizations, /notificacoes, /planos
test_mapas.py         7    CRUD + 404s
test_stats.py         5    stats, statstpuser, registrations + no auth
test_tipouser.py      6    CRUD + 404s
test_utilizadores.py  4    CRUD + 404
test_webhooks.py     15    webhook validation, checkout flow, Celery tasks
```

</details>

---

## Quick Start

```bash
git clone https://github.com/Wand-DenaXy/-Manueli-s-Clubes.git && cd -Manueli-s-Clubes
docker compose up --build
# http://localhost:3000 (frontend)   http://localhost:8000/docs (API)
```

---

## Screenshots

<img width="1000" height="500" alt="Dashboard" src="nuxt-app/assets/images/DashboardManuel.PNG" />

> **Dashboard** — KPIs + Chart.js (line + doughnut). Cache Redis.

<img width="1000" height="500" alt="Mapas" src="nuxt-app/assets/images/ManuelMapas.PNG" />

> **Mapa** — Leaflet.js, marcadores GPS, painel lateral.

<img width="1000" height="500" alt="Login" src="nuxt-app/assets/images/ManuelLogin.PNG" />

> **Login** — 3 roles · Argon2id · JWT 30 min.

---

<details>
<summary><strong>Estrutura do Projeto</strong></summary>

```
-Manueli-s-Clubes/
├── docker-compose.yml               # Orquestração: db + redis + api + worker + frontend
├── .env                             # Variáveis para Docker Compose (MYSQL_USER, etc.)
├── package.json                     # deps globais (Bootstrap, Chart.js, Leaflet)
├── .github/
│   └── workflows/
│       └── ci.yml                   # CI pipeline: testes + lint + Docker build
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
│   └── tests/                       # 72 testes (pytest + httpx)
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_clubes.py
│       ├── test_email.py
│       ├── test_endpoints.py
│       ├── test_mapas.py
│       ├── test_stats.py
│       ├── test_tipouser.py
│       ├── test_utilizadores.py
│       └── test_webhooks.py
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

</details>

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

Redis serve como cache (`SETEX` + `SCAN`/`DEL` por prefixo) e Celery broker numa única instância.

| Recurso          | Cache Key              | TTL    | Invalidado por       |
|------------------|------------------------|--------|----------------------|
| `/stats`         | `stats`                | 60 s   | CRUD clubes/users    |
| `/clubes`        | `clubes:org:{id}:list` | 30 s   | CRUD clubes          |
| `/tipouser`      | `tipouser:list`        | 120 s  | CRUD tipouser        |
| `/mapas`         | `mapas:list`           | 60 s   | CRUD mapas           |
| `/planos`        | `planos:list`          | 120 s  | CRUD planos          |
| `/utilizadores`  | `utilizadores:list`    | 30 s   | PUT /me/plano, DEL   |

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
<summary><strong>Testes — Detalhe</strong></summary>

### Estratégia

- **SQLite** para BD de testes (sem PostgreSQL)
- **Redis mockado** no conftest (`_redis = MagicMock()`) — testes passam sem Redis local
- **Redis service container** no CI (GitHub Actions)
- **Dependency override** do `get_db` para injetar sessão de teste
- **Celery tasks** testadas diretamente (sem broker) com `SessionLocal` mockado
- Startup event desativado em testes (`on_startup.clear()`)
- Coverage gate: build falha se < 75%

### Edge Cases Testados

| Cenário | Status Code | Ficheiro |
|---------|-------------|----------|
| Token JWT forjado/adulterado | 401 | `test_auth.py` |
| Login com utilizador inexistente | 401 | `test_auth.py` |
| Acesso a rota protegida sem token | 401 | `test_auth.py` |
| Username duplicado no registo | 400 | `test_auth.py` |
| Limite de clubes do plano atingido | 403 | `test_clubes.py` |
| Inscrição duplicada em clube (UniqueConstraint) | 409 | `test_clubes.py` |
| CRUD em recurso inexistente (clube, mapa, tipo, user, plano) | 404 | `test_*.py` |
| Webhook secret vazio (não configurado) | 500 | `test_webhooks.py` |
| Payload Stripe inválido | 400 | `test_webhooks.py` |
| Assinatura Stripe inválida (HMAC) | 400 | `test_webhooks.py` |
| Evento webhook duplicado (idempotência) | 200 duplicate | `test_webhooks.py` |
| Checkout em plano gratuito (preço = 0) | 400 | `test_webhooks.py` |
| Stripe API error durante checkout | 502 | `test_webhooks.py` |
| Task: evento duplicado no Celery worker | skipped | `test_webhooks.py` |
| Task: metadata incompleta no checkout | skipped | `test_webhooks.py` |
| Task: user não encontrado no payment_failed | skipped | `test_webhooks.py` |
| SMTP não configurado | False (no-op) | `test_email.py` |
| Falha de envio SMTP | False | `test_email.py` |

</details>

<details>
<summary><strong>Decisões Técnicas (ADR)</strong></summary>

| Decisão | Porquê |
|---------|--------|
| **FastAPI** vs Django/Flask | OpenAPI automático, validação Pydantic nativa, DI com `Depends()`, ASGI async |
| **Argon2id** vs bcrypt | Vencedor da PHC, resistente a GPU/ASIC |
| **Stripe Checkout** (hosted) | Zero PCI compliance, subscrições recorrentes com redirect flow |
| **Celery + Redis** para webhooks | Resposta < 200 ms ao Stripe, retry com backoff, idempotência por `event_id` |
| **Multi-tenancy** por organização | `WHERE organization_id = user.organization_id` em queries, sem schema separation |
| **RBAC** via `require_roles()` | FastAPI Dependency, enforcement server-side (3 roles: Admin/Gestor/Cliente) |
| **UniqueConstraint** em `membro_clube` | Anti-duplicação a nível de BD, catch `IntegrityError` → 409 |

</details>

<details>
<summary><strong>Docker — Visão Geral</strong></summary>

| Serviço    | Imagem             | Porta | Função                            |
|------------|--------------------| ------|-----------------------------------|
| `db`       | `postgres:15`      | 5432  | PostgreSQL + healthcheck          |
| `redis`    | `redis:7-alpine`   | 6379  | Cache + Celery broker             |
| `api`      | `python:3.11-slim` | 8000  | FastAPI + Uvicorn                 |
| `worker`   | `python:3.11-slim` | —     | Celery worker (webhooks + emails) |
| `frontend` | `node:20`          | 3000  | Nuxt 3 SSR                        |

```bash
docker compose up --build        # sobe os 5 containers
docker compose logs -f api       # logs do backend
```

```mermaid
graph LR
    subgraph clubes_net [Docker Network]
        DB["db :5432"]
        RD["redis :6379"]
        API["api :8000"]
        WK["worker"]
        FE["frontend :3000"]
    end
    FE --> API --> DB
    API --> RD
    WK --> DB
    WK --> RD
```

</details>

<details>
<summary><strong>Setup Local (sem Docker)</strong></summary>

```bash
# Copiar .env de exemplo e preencher
cp api/.env.example api/.env

# Backend
cd api/app && pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
# → http://localhost:8000/docs

# Worker (noutra tab)
cd api && celery -A app.celery_app:celery worker --loglevel=info

# Frontend (noutra tab)
cd nuxt-app && npm install && npm run dev
# → http://localhost:3000

# Stripe webhooks locais (noutra tab)
stripe listen --forward-to localhost:8000/stripe/webhook
```

Variáveis necessárias: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `SECRET_KEY`, `ALGORITHM`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `REDIS_URL`, `SMTP_*`.

</details>

---

## Autor

**Manuel Silvestre**
