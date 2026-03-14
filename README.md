# Manueli's Clubes

**Plataforma full-stack de gestão de clubes** — criar clubes, gerir membros, visualizar eventos no calendário e localizar pontos no mapa interativo.

<img width="1000" height="500" alt="ManueliClube" src="https://github.com/user-attachments/assets/786aee57-cdbc-4be2-823b-51c221d7e4b8" />

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white" />
  <img alt="Nuxt" src="https://img.shields.io/badge/Nuxt-4.3-00DC82?logo=nuxtdotjs&logoColor=white" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" />
  <img alt="JWT" src="https://img.shields.io/badge/Auth-JWT%20+%20Argon2-000000?logo=jsonwebtokens&logoColor=white" />
  <img alt="Tests" src="https://img.shields.io/badge/Tests-35%20passed-brightgreen?logo=pytest&logoColor=white" />
</p>

---

## Funcionalidades

### Dashboard — KPIs e Gráficos em Tempo Real

Painel de administração com 3 cards de métricas (clubes, utilizadores, mapas), gráfico de linha (registos mensais) e doughnut (distribuição por tipo de utilizador) — tudo alimentado pela API com cache.

<!-- 📸 SCREENSHOT: Dashboard com sidebar escura à esquerda, 3 KPI cards no topo (Clubes, Utilizadores, Mapas com ícones e contadores), gráfico de linha Chart.js (registos mensais) à esquerda e gráfico doughnut (distribuição por tipo de user) à direita. Fundo escuro (#1a1a2e). -->

<img width="1000" height="500" alt="Dashboard" src="nuxt-app/assets/images/DashboardManuel.PNG" />

---

### Gestão de Clubes — CRUD Completo

Tabela interativa com criação, edição inline e eliminação — permissões por tipo de utilizador (admin vê tudo, gestor pode editar). SweetAlert2 para confirmações.

<!-- 📸 SCREENSHOT: Formulário escuro com 4 campos (nome, email, telefone, localidade) + botão "Guardar", seguido de tabela responsiva com colunas (nome, email, telefone, localidade, ações) e botões Editar/Eliminar por linha. -->

---

### Mapa Interativo — Leaflet.js

Mapa dark-themed com marcadores dos clubes, painel lateral com lista de pontos e formulário para adicionar novas localizações por coordenadas GPS.

<!-- 📸 SCREENSHOT: Layout 3 painéis — lista à esquerda, mapa Leaflet ao centro (basemap escuro CartoDB dark_all com marcadores), formulário à direita (descrição, latitude, longitude, dropdown clube_id). -->

<img width="1000" height="500" alt="Mapas" src="nuxt-app/assets/images/ManuelMapas.PNG" />

---

### Calendário de Eventos — FullCalendar

Calendário mensal com eventos dos clubes em cores diferentes. Clicar num evento abre um painel com detalhes e botão "Ingressar" — inscrição com proteção de duplicação (HTTP 409).

<!-- 📸 SCREENSHOT: Grelha FullCalendar mensal com blocos de eventos coloridos. Painel slide-in à direita com nome do clube, data, localidade e botão "Ingressar". -->

---

### Autenticação — JWT + Argon2

Login com username, password e seleção de tipo de utilizador. Passwords hashed com Argon2id. Token JWT (30 min) enviado no header `Authorization: Bearer`.

<!-- 📸 SCREENSHOT: Layout 50/50 — formulário escuro à esquerda (username, password, dropdown tipo) com botão "Login", imagem/banner à direita. -->

<img width="1000" height="500" alt="Login" src="nuxt-app/assets/images/ManuelLogin.PNG" />

---

### Landing Page e About Us

Página inicial com hero section, call-to-action e barra de estatísticas em tempo real (total de clubes, utilizadores, mapas). Página "Sobre nós" com missão, valores e equipa.

<!-- 📸 SCREENSHOT: Hero escuro com título grande, subtítulo, 2 botões CTA (Login / Ver Clubes) e barra de stats (3 contadores animados). -->

---

## Quick Start

```bash
# 1. Clonar
git clone https://github.com/<user>/Manueli-s-Clubes.git
cd Manueli-s-Clubes

# 2. Configurar variáveis de ambiente
#    → .env (raiz): DB_USER, DB_PASSWORD, DB_NAME
#    → api/.env:   MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, SECRET_KEY, ALGORITHM

# 3. Lançar tudo
docker compose up --build
```

| Serviço    | URL                          |
|------------|------------------------------|
| Frontend   | http://localhost:3000         |
| API (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432               |

---

## Testes — 35/35 Passed

```bash
cd api && pytest tests/ -v --tb=short
```

```
tests/test_auth.py         ✅ 5 passed   (registo, login, token, password errada, rota protegida)
tests/test_clubes.py       ✅ 8 passed   (CRUD + inscrição + duplicação 409 + 404)
tests/test_utilizadores.py ✅ 4 passed   (list, update, delete, 404)
tests/test_tipouser.py     ✅ 6 passed   (CRUD + 404)
tests/test_mapas.py        ✅ 7 passed   (CRUD + clube inexistente + 404)
tests/test_stats.py        ✅ 5 passed   (stats, statstpuser, registrations, auth guard)
```

---

## Tech Stack

| Camada     | Tecnologia                         | Versão    |
|------------|------------------------------------|-----------|
| Runtime    | Python                             | 3.11      |
| API        | FastAPI + Uvicorn                  | 0.115.6   |
| ORM        | SQLAlchemy                         | 2.0.36    |
| DB         | PostgreSQL (psycopg2)              | 15+       |
| Auth       | python-jose (JWT) + Argon2         | —         |
| Cache      | In-memory dict (TTL + invalidação) | —         |
| Frontend   | Nuxt 4 (Vue 3, SSR)               | 4.3.x     |
| UI         | Bootstrap 5, SweetAlert2           | —         |
| Viz        | Chart.js, Leaflet.js, FullCalendar | —         |
| Container  | Docker + Docker Compose            | —         |

---

## Estrutura do Projeto

```
-Manueli-s-Clubes/
├── docker-compose.yml               # Orquestração: db + api + frontend
├── package.json                     # deps globais (Bootstrap, Chart.js, Leaflet)
│
├── api/                             # Backend (FastAPI)
│   ├── Dockerfile                   # python:3.11-slim → uvicorn :8000
│   ├── app/
│   │   ├── main.py                  # CRUD routes, stats, inscrições, cache
│   │   ├── auth.py                  # JWT + Argon2
│   │   ├── models.py               # ORM + Pydantic schemas
│   │   ├── database.py             # PostgreSQL connection
│   │   ├── cache.py                # TTL + invalidação por prefixo
│   │   └── requirements.txt
│   └── tests/                       # 35 testes (pytest + httpx)
│
└── nuxt-app/                        # Frontend (Nuxt 4)
    ├── Dockerfile                   # node:20 → :3000
    ├── pages/
    │   ├── index.vue                # Landing — stats públicas
    │   ├── login.vue                # Auth
    │   ├── dashboard.vue            # KPIs + Chart.js
    │   ├── clubes.vue               # CRUD table
    │   ├── mapas.vue                # Leaflet map
    │   ├── calendario.vue           # FullCalendar + inscrição
    │   └── aboutus.vue              # Sobre nós
    └── components/Header.vue        # Nav global
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
    System(sys, "Manueli's Clubes", "Plataforma de gestão de clubes")
    SystemDb(db, "PostgreSQL", "Armazenamento persistente")

    Rel(user, sys, "HTTPS / JSON")
    Rel(sys, db, "SQL via SQLAlchemy ORM")
```

### Nível 2 — Containers

```mermaid
C4Container
    title Container Diagram — Manueli's Clubes

    Person(user, "Utilizador")

    Container_Boundary(frontend, "Frontend") {
        Container(nuxt, "Nuxt 4 App", "Vue 3, SSR, Nitro", "SPA/SSR servida ao browser. Routing por ficheiro, Composition API.")
    }

    Container_Boundary(backend, "Backend") {
        Container(api, "FastAPI", "Python 3.10+, Uvicorn", "API REST. Auth JWT, CRUD, inscrições, stats. Cache in-memory com TTL.")
        Container(auth_mod, "Auth Module", "python-jose, passlib[argon2]", "Registo, login, emissão/validação JWT.")
        Container(cache_mod, "Cache Module", "cache.py, dict + time.monotonic", "Cache in-memory com TTL por key e invalidação por prefixo.")
    }

    ContainerDb(db, "PostgreSQL", "psycopg2", "5 tabelas: clubes, utilizador, tipouser, mapas, membro_clube")

    Rel(user, nuxt, "HTTPS :3000")
    Rel(nuxt, api, "fetch HTTP/JSON :8000", "Authorization: Bearer JWT")
    Rel(api, auth_mod, "Depends(get_current_user)")
    Rel(api, cache_mod, "cache_get / cache_set / cache_invalidate")
    Rel(api, db, "SQLAlchemy Session")
    Rel(auth_mod, db, "SQLAlchemy Session")
```

### Nível 3 — Componentes (API)

```mermaid
C4Component
    title Component Diagram — FastAPI Backend

    Container_Boundary(api, "FastAPI Application") {
        Component(main, "main.py", "FastAPI Router", "CRUD clubes/utilizadores/tipouser/mapas + stats + inscrições. CORS middleware. Cache get/set nos GETs, invalidate nos writes. Startup init_db().")
        Component(auth, "auth.py", "APIRouter /auth", "POST /auth/ (register), POST /auth/token (login). Argon2 hash/verify. JWT encode/decode. get_current_user dependency.")
        Component(models, "models.py", "SQLAlchemy + Pydantic", "5 ORM models + relationships + cascade config. Pydantic schemas para request/response validation.")
        Component(database, "database.py", "Engine + SessionLocal", "Connection string via env vars. get_db() generator. init_db() → Base.metadata.create_all().")
        Component(cache, "cache.py", "dict + TTL", "cache_get(key), cache_set(key, value, ttl), cache_invalidate(*prefixes). TTL via time.monotonic().")
    }

    ContainerDb(db, "PostgreSQL")

    Rel(main, auth, "include_router(auth.router)")
    Rel(main, models, "importa Models + Schemas")
    Rel(main, database, "Depends(get_db)")
    Rel(main, cache, "cache_get / cache_set / cache_invalidate")
    Rel(auth, models, "importa UtilizadorModel")
    Rel(auth, database, "SessionLocal()")
    Rel(database, db, "psycopg2 connection pool")
```

</details>

<details>
<summary><strong>Modelo de Dados (ER)</strong></summary>

```mermaid
erDiagram
    tipouser ||--o{ utilizador : "1:N"
    utilizador ||--o{ membro_clube : "1:N"
    clubes ||--o{ membro_clube : "1:N"
    clubes ||--o{ mapas : "1:N"

    tipouser {
        int id PK
        varchar(100) descricao
    }

    utilizador {
        int id PK
        varchar(50) username UK
        varchar(255) password
        datetime created_at
        int tipo_id FK
    }

    clubes {
        int id PK
        varchar(100) nome
        varchar(150) email UK
        varchar(20) telefone
        varchar(100) localidade
        date evento_at
        datetime created_at
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
```

> **Constraint:** `UniqueConstraint("utilizador_id", "clube_id")` em `membro_clube` — impede inscrição duplicada a nível de BD.

</details>

<details>
<summary><strong>Cache — Estratégia de TTL e Invalidação</strong></summary>

O sistema usa cache in-memory (`cache.py`) com TTL por key e invalidação automática por prefixo em operações de escrita.

### Módulo `cache.py`

```python
import time
from typing import Any

_cache: dict[str, tuple[float, Any]] = {}

def cache_get(key: str) -> Any | None:
    entry = _cache.get(key)
    if entry is None:
        return None
    expires_at, value = entry
    if time.monotonic() > expires_at:
        del _cache[key]
        return None
    return value

def cache_set(key: str, value: Any, ttl: int) -> None:
    _cache[key] = (time.monotonic() + ttl, value)

def cache_invalidate(*prefixes: str) -> None:
    keys_to_delete = [k for k in _cache if any(k.startswith(p) for p in prefixes)]
    for k in keys_to_delete:
        del _cache[k]
```

### Tabela de TTL e Invalidação

| Endpoint GET        | Cache Key              | TTL    | Invalidado por                           |
|---------------------|------------------------|--------|------------------------------------------|
| `GET /stats`        | `stats`                | 60 s   | POST/PUT/DELETE clubes, utilizadores, mapas, tipouser |
| `GET /statstpuser`  | `statstpuser`          | 60 s   | POST/PUT/DELETE utilizadores, tipouser   |
| `GET /registrations`| `registrations:{year}` | 300 s  | DELETE/PUT utilizadores                  |
| `GET /clubes`       | `clubes:list`          | 30 s   | POST/PUT/DELETE clubes                   |
| `GET /tipouser`     | `tipouser:list`        | 120 s  | POST/PUT/DELETE tipouser                 |
| `GET /mapas`        | `mapas:list`           | 60 s   | POST/PUT/DELETE mapas                    |

### Fluxo de Leitura (GET)

```python
cached = cache_get("stats")
if cached is not None:
    return cached          # responde sem tocar na BD
result = { ... }          # query à BD
cache_set("stats", result, ttl=60)
return result
```

### Fluxo de Escrita (POST/PUT/DELETE)

```python
cache_invalidate("stats", "clubes:")
# Remove todas as keys que começam com "stats" ou "clubes:"
```

</details>

<details>
<summary><strong>Endpoints da API</strong></summary>

### Auth (`/auth`)

| Método | Rota           | Body / Params                              | Response          | Auth |
|--------|----------------|--------------------------------------------|-------------------|------|
| POST   | `/auth/`       | `{username, password, tipo_id}`            | `201` message     | —    |
| POST   | `/auth/token`  | FormData: `username, password, tipo_id`    | `{access_token, token_type}` | — |

### Clubes (`/clubes`)

| Método | Rota                     | Body / Params       | Response            | Auth  | Status Codes     | Cache                              |
|--------|--------------------------|---------------------|---------------------|-------|------------------|------------------------------------|
| POST   | `/clubes`                | `ClubeCreate`       | `ClubeResponse`     | JWT   | 200              | invalidate `stats`, `clubes:`      |
| GET    | `/clubes`                | —                   | `[ClubeResponse]`   | JWT   | 200              | `clubes:list` TTL 30 s             |
| PUT    | `/clubes/{id}`           | `ClubeCreate`       | `ClubeResponse`     | JWT   | 200, 404         | invalidate `stats`, `clubes:`      |
| DELETE | `/clubes/{id}`           | —                   | —                   | JWT   | 204, 404         | invalidate `stats`, `clubes:`      |
| POST   | `/clubes/{id}/ingressar` | —                   | `IngressarResponse` | JWT   | 201, 404, 409    | —                                  |

### Utilizadores (`/utilizadores`)

| Método | Rota                  | Body / Params       | Response               | Auth | Status Codes | Cache                                        |
|--------|-----------------------|---------------------|------------------------|------|--------------|----------------------------------------------|
| GET    | `/utilizadores`       | —                   | `[UtilizadorResponse]` | JWT  | 200          | `utilizadores:list` TTL 30 s                 |
| PUT    | `/utilizadores/{id}`  | `UtilizadorCreate`  | `UtilizadorResponse`   | JWT  | 200, 404     | invalidate `stats`, `statstpuser`            |
| DELETE | `/utilizadores/{id}`  | —                   | —                      | JWT  | 204, 404     | invalidate `stats`, `statstpuser`, `registrations:` |

### Tipos de Utilizador (`/tipouser`)

| Método | Rota              | Body / Params    | Response             | Auth | Status Codes | Cache                                         |
|--------|--------------------|------------------|----------------------|------|--------------|-----------------------------------------------|
| POST   | `/tipouser`        | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200          | invalidate `stats`, `statstpuser`, `tipouser:` |
| GET    | `/tipouser`        | —                | `[TipoUserResponse]` | —    | 200          | `tipouser:list` TTL 120 s                     |
| PUT    | `/tipouser/{id}`   | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200, 404     | invalidate `stats`, `statstpuser`, `tipouser:` |
| DELETE | `/tipouser/{id}`   | —                | —                    | JWT  | 204, 404     | invalidate `stats`, `statstpuser`, `tipouser:` |

### Mapas (`/mapas`)

| Método | Rota           | Body / Params | Response          | Auth | Status Codes | Cache                          |
|--------|----------------|---------------|-------------------|------|--------------|--------------------------------|
| POST   | `/mapas`       | `MapaCreate`  | `MapaResponse`    | JWT  | 200, 404     | invalidate `stats`, `mapas:`   |
| GET    | `/mapas`       | —             | `[MapaResponse]`  | JWT  | 200          | `mapas:list` TTL 60 s          |
| PUT    | `/mapas/{id}`  | `MapaCreate`  | `MapaResponse`    | JWT  | 200, 404     | invalidate `stats`, `mapas:`   |
| DELETE | `/mapas/{id}`  | —             | message           | JWT  | 200, 404     | invalidate `stats`, `mapas:`   |

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
# Request
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

# Response
class ClubeResponse(ClubeCreate):        # herda campos + id
    id: int

class UtilizadorResponse(BaseModel):      # inclui nested TipoUserResponse
    id: int
    username: str
    tipo: TipoUserResponse
    created_at: datetime

class MapaResponse(BaseModel):
    id: int
    descricao: str | None = None
    latitude: float
    longitude: float
    clube_id: int

class IngressarResponse(BaseModel):
    mensagem: str
    clube_id: int
    clube_nome: str
    inscrito_em: datetime
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

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant F as Nuxt Frontend
    participant A as FastAPI /auth
    participant DB as PostgreSQL
    Note over F,A: Pedidos subsequentes — header Authorization enviado pelo frontend

    F->>A: GET /clubes (Authorization: Bearer token)
    A->>A: jwt.decode(token, SECRET_KEY, [HS256])
    alt Token inválido/expirado
        A-->>F: 401 Unauthorized
    else Token válido
        A->>DB: SELECT * FROM clubes
        DB-->>A: [rows]
        A-->>F: 200 [ClubeResponse]
    end
```

### CRUD — Criar Clube (com invalidação de cache)

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant F as Nuxt (clubes.vue)
    participant API as FastAPI
    participant C as Cache (dict)
    participant DB as PostgreSQL

    U->>F: Preenche formulário (nome, email, tel, localidade, evento_at)
    F->>API: POST /clubes {ClubeCreate} + Bearer JWT
    API->>API: Depends(get_current_user) → valida JWT
    API->>DB: INSERT INTO clubes VALUES(...)
    DB-->>API: clube row
    API->>C: cache_invalidate("stats", "clubes:")
    C->>C: Remove keys com prefixo "stats" e "clubes:"
    API-->>F: 200 ClubeResponse {id, nome, ...}
    F->>F: Swal.fire("Sucesso")
    F->>API: GET /clubes + Bearer JWT
    API->>C: cache_get("clubes:list")
    C-->>API: None (cache miss)
    API->>DB: SELECT * FROM clubes
    DB-->>API: [rows]
    API->>C: cache_set("clubes:list", rows, ttl=30)
    API-->>F: 200 [ClubeResponse]
    F->>F: Atualiza tabela reativa
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

### Dashboard — Carregamento de Estatísticas (com cache)

```mermaid
sequenceDiagram
    participant F as Nuxt (dashboard.vue)
    participant API as FastAPI
    participant C as Cache (dict)
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

| Módulo       | Cobertura Alvo |
|--------------|----------------|
| `auth.py`    | ≥ 90%          |
| `main.py`    | ≥ 85%          |
| `models.py`  | ≥ 95%          |
| `database.py`| ≥ 80%          |
| `cache.py`   | ≥ 90%          |

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

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {"username": payload.get("sub"), "id": payload.get("id"), "tipo_id": payload.get("tipo_id")}
```

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

### ADR-008: Cache in-memory com TTL

**Status:** Aceite  
**Decisão:** `dict` Python com `time.monotonic()`. Zero dependências externas, latência ~0 para cache hits, invalidação por prefixo em writes. Redis evitado por overhead operacional desnecessário para single-instance.

</details>

<details>
<summary><strong>Docker — Configuração Completa</strong></summary>

### Serviços

| Serviço    | Imagem Base        | Container          | Porta  | Descrição                              |
|------------|--------------------|--------------------|--------|----------------------------------------|
| `db`       | `postgres:15`      | `clubes_db`        | 5432   | PostgreSQL com volume persistente      |
| `api`      | `python:3.11-slim` | `clubes_api`       | 8000   | FastAPI + Uvicorn                      |
| `frontend` | `node:20`          | `clubes_frontend`  | 3000   | Nuxt 4 (build + dev)                   |

### `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:15
    container_name: clubes_db
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: ./api
    container_name: clubes_api
    ports:
      - "8000:8000"
    env_file:
      - ./api/.env
    environment:
      MYSQL_HOST: host.docker.internal
      MYSQL_PORT: 5432
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}

  frontend:
    build: ./nuxt-app
    container_name: clubes_frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  postgres_data:
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
    subgraph Docker Network
        DB["clubes_db<br/>postgres:15<br/>:5432"]
        API["clubes_api<br/>python:3.11-slim<br/>:8000"]
        FE["clubes_frontend<br/>node:20<br/>:3000"]
    end

    FE -->|depends_on| API
    API -->|host.docker.internal:5432| DB
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
MYSQL_DATABASE=clubes_db
SECRET_KEY=<random-256-bit-hex>
ALGORITHM=HS256
```

**`.env`** (raiz) — Docker Compose:
```env
DB_USER=<user>
DB_PASSWORD=<password>
DB_NAME=clubes_db
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
