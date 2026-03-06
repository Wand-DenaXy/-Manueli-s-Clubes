# Manueli's Clubes

Plataforma web full-stack de gestão de clubes — **Nuxt 4** + **FastAPI** + **PostgreSQL**.

<img width="1000" height="500" alt="ManueliClube" src="https://github.com/user-attachments/assets/786aee57-cdbc-4be2-823b-51c221d7e4b8" />

---

## Tech Stack

| Camada     | Tecnologia                    | Versão    |
|------------|-------------------------------|-----------|
| Runtime    | Python                        | 3.10+     |
| API        | FastAPI + Uvicorn              | 0.115.6   |
| ORM        | SQLAlchemy                     | 2.0.36    |
| DB         | PostgreSQL (psycopg2)          | 15+       |
| Auth       | python-jose (JWT) + Argon2     | —         |
| Frontend   | Nuxt 4 (Vue 3, SSR)           | 4.x       |
| UI         | Bootstrap 5, SweetAlert2       | —         |
| Viz        | Chart.js, Leaflet.js, FullCalendar | —     |

---

## Arquitetura — Diagramas C4

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
        Container(api, "FastAPI", "Python 3.10+, Uvicorn", "API REST. Auth JWT, CRUD, inscrições, stats.")
        Container(auth_mod, "Auth Module", "python-jose, passlib[argon2]", "Registo, login, emissão/validação JWT.")
    }

    ContainerDb(db, "PostgreSQL", "psycopg2", "5 tabelas: clubes, utilizador, tipouser, mapas, membro_clube")

    Rel(user, nuxt, "HTTPS :3000")
    Rel(nuxt, api, "fetch HTTP/JSON :8000", "Bearer JWT")
    Rel(api, auth_mod, "Depends(get_current_user)")
    Rel(api, db, "SQLAlchemy Session")
    Rel(auth_mod, db, "SQLAlchemy Session")
```

### Nível 3 — Componentes (API)

```mermaid
C4Component
    title Component Diagram — FastAPI Backend

    Container_Boundary(api, "FastAPI Application") {
        Component(main, "main.py", "FastAPI Router", "CRUD clubes/utilizadores/tipouser/mapas + stats + inscrições. CORS middleware. Startup init_db().")
        Component(auth, "auth.py", "APIRouter /auth", "POST /auth/ (register), POST /auth/token (login). Argon2 hash/verify. JWT encode/decode. get_current_user dependency.")
        Component(models, "models.py", "SQLAlchemy + Pydantic", "5 ORM models + relationships + cascade config. Pydantic schemas para request/response validation.")
        Component(database, "database.py", "Engine + SessionLocal", "Connection string via env vars. get_db() generator. init_db() → Base.metadata.create_all().")
    }

    ContainerDb(db, "PostgreSQL")

    Rel(main, auth, "include_router(auth.router)")
    Rel(main, models, "importa Models + Schemas")
    Rel(main, database, "Depends(get_db)")
    Rel(auth, models, "importa UtilizadorModel")
    Rel(auth, database, "SessionLocal()")
    Rel(database, db, "psycopg2 connection pool")
```

---

## Modelo de Dados (ER)

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

---

## Sequence Diagrams

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
        A-->>F: 200 {access_token, token_type: "bearer"}
    end

    F->>F: localStorage.setItem("token", access_token)
    F->>F: navigateTo("/dashboard")

    Note over F,A: Pedidos subsequentes

    F->>A: GET /clubes (Authorization: Bearer <JWT>)
    A->>A: jwt.decode(token) → {sub, id, tipo_id}
    alt Token inválido/expirado
        A-->>F: 401 Unauthorized
    else Token válido
        A->>DB: SELECT * FROM clubes
        DB-->>A: [rows]
        A-->>F: 200 [ClubeResponse]
    end
```

### CRUD — Criar Clube

```mermaid
sequenceDiagram
    actor U as Utilizador
    participant F as Nuxt (clubes.vue)
    participant API as FastAPI
    participant DB as PostgreSQL

    U->>F: Preenche formulário (nome, email, tel, localidade, evento_at)
    F->>API: POST /clubes {ClubeCreate} + Bearer JWT
    API->>API: Depends(get_current_user) → valida JWT
    API->>DB: INSERT INTO clubes VALUES(...)
    DB-->>API: clube row
    API-->>F: 200 ClubeResponse {id, nome, ...}
    F->>F: Swal.fire("Sucesso")
    F->>API: GET /clubes + Bearer JWT
    API->>DB: SELECT * FROM clubes
    DB-->>API: [rows]
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

### Dashboard — Carregamento de Estatísticas

```mermaid
sequenceDiagram
    participant F as Nuxt (dashboard.vue)
    participant API as FastAPI
    participant DB as PostgreSQL

    F->>API: GET /stats
    API->>DB: SELECT COUNT(*) FROM clubes, utilizador, tipouser, mapas
    DB-->>API: {counts}
    API-->>F: {clubes, utilizadores, tipousers, mapas}

    par Parallel requests
        F->>API: GET /statstpuser + Bearer JWT
        API->>DB: GROUP BY tipo_id → COUNT(*)
        DB-->>API: {tipo: count}
        API-->>F: {admin: N, gestor: N, ...}
    and
        F->>API: GET /registrations + Bearer JWT
        API->>DB: SELECT EXTRACT(month), COUNT(*) WHERE year = current GROUP BY month
        DB-->>API: [{month, count}]
        API-->>F: [{month: "Janeiro", count: N}, ...]
    end

    F->>F: Chart.js render (line + doughnut)
```

---

## Endpoints da API

### Auth (`/auth`)

| Método | Rota           | Body / Params                              | Response          | Auth |
|--------|----------------|--------------------------------------------|-------------------|------|
| POST   | `/auth/`       | `{username, password, tipo_id}`            | `201` message     | —    |
| POST   | `/auth/token`  | FormData: `username, password, tipo_id`    | `{access_token, token_type}` | — |

### Clubes (`/clubes`)

| Método | Rota                     | Body / Params       | Response            | Auth  | Status Codes     |
|--------|--------------------------|---------------------|---------------------|-------|------------------|
| POST   | `/clubes`                | `ClubeCreate`       | `ClubeResponse`     | JWT   | 200              |
| GET    | `/clubes`                | —                   | `[ClubeResponse]`   | JWT   | 200              |
| PUT    | `/clubes/{id}`           | `ClubeCreate`       | `ClubeResponse`     | JWT   | 200, 404         |
| DELETE | `/clubes/{id}`           | —                   | —                   | JWT   | 204, 404         |
| POST   | `/clubes/{id}/ingressar` | —                   | `IngressarResponse` | JWT   | 201, 404, 409    |

### Utilizadores (`/utilizadores`)

| Método | Rota                  | Body / Params       | Response               | Auth | Status Codes |
|--------|-----------------------|---------------------|------------------------|------|--------------|
| GET    | `/utilizadores`       | —                   | `[UtilizadorResponse]` | JWT  | 200          |
| PUT    | `/utilizadores/{id}`  | `UtilizadorCreate`  | `UtilizadorResponse`   | JWT  | 200, 404     |
| DELETE | `/utilizadores/{id}`  | —                   | —                      | JWT  | 204, 404     |

### Tipos de Utilizador (`/tipouser`)

| Método | Rota              | Body / Params    | Response             | Auth | Status Codes |
|--------|--------------------|------------------|----------------------|------|--------------|
| POST   | `/tipouser`        | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200          |
| GET    | `/tipouser`        | —                | `[TipoUserResponse]` | —    | 200          |
| PUT    | `/tipouser/{id}`   | `TipoUserCreate` | `TipoUserResponse`  | JWT  | 200, 404     |
| DELETE | `/tipouser/{id}`   | —                | —                    | JWT  | 204, 404     |

### Mapas (`/mapas`)

| Método | Rota           | Body / Params | Response          | Auth | Status Codes |
|--------|----------------|---------------|-------------------|------|--------------|
| POST   | `/mapas`       | `MapaCreate`  | `MapaResponse`    | JWT  | 200, 404     |
| GET    | `/mapas`       | —             | `[MapaResponse]`  | JWT  | 200          |
| PUT    | `/mapas/{id}`  | `MapaCreate`  | `MapaResponse`    | JWT  | 200, 404     |
| DELETE | `/mapas/{id}`  | —             | message           | JWT  | 200, 404     |

### Estatísticas

| Método | Rota             | Response                                        | Auth |
|--------|-------------------|-------------------------------------------------|------|
| GET    | `/stats`          | `{clubes, utilizadores, tipousers, mapas}`      | —    |
| GET    | `/statstpuser`    | `{tipo_descricao: count, ...}`                  | JWT  |
| GET    | `/registrations`  | `[{month: str, count: int}]` (12 meses)        | JWT  |

---

## Pydantic Schemas (Contratos)

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

class IngressarResponse(BaseModel):       # resposta de inscrição
    mensagem: str
    clube_id: int
    clube_nome: str
    inscrito_em: datetime
```

---

## Testes

### Estrutura de Testes (pytest + httpx)

```
api/
├── tests/
│   ├── conftest.py          # Fixtures: TestClient, BD em memória, token helper
│   ├── test_auth.py         # Registo, login, token inválido
│   ├── test_clubes.py       # CRUD clubes + inscrição + duplicação
│   ├── test_utilizadores.py # CRUD utilizadores
│   ├── test_tipouser.py     # CRUD tipos
│   ├── test_mapas.py        # CRUD mapas
│   └── test_stats.py        # Endpoints de estatísticas
```

### `conftest.py` — Fixtures

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Regista utilizador e devolve headers com JWT."""
    client.post("/tipouser", json={"descricao": "admin"},
                headers=_get_temp_token(client))
    client.post("/auth/", json={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": 1})
    resp = client.post("/auth/token", data={"username": "testuser", "password": "Str0ng!Pass", "tipo_id": "1"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### `test_auth.py` — Autenticação

```python
def test_register_success(client):
    # Arrange: criar tipo primeiro
    # ...setup tipo_id=1...
    
    # Act
    resp = client.post("/auth/", json={
        "username": "newuser",
        "password": "Str0ng!Pass",
        "tipo_id": 1
    })
    
    # Assert
    assert resp.status_code == 201
    assert resp.json()["message"] == "Utilizador Criado com Sucesso"


def test_register_duplicate_username(client):
    # Registar 2x o mesmo username → 400
    client.post("/auth/", json={"username": "dup", "password": "Pass1!", "tipo_id": 1})
    resp = client.post("/auth/", json={"username": "dup", "password": "Pass2!", "tipo_id": 1})
    assert resp.status_code == 400


def test_login_returns_jwt(client):
    # ...após registo...
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": "1"
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "wrong",
        "tipo_id": "1"
    })
    assert resp.status_code == 401


def test_protected_route_without_token(client):
    resp = client.get("/clubes")
    assert resp.status_code == 401
```

### `test_clubes.py` — CRUD + Inscrição

```python
def test_create_clube(client, auth_headers):
    resp = client.post("/clubes", json={
        "nome": "Clube Teste",
        "email": "teste@clube.pt",
        "telefone": "912345678",
        "localidade": "Lisboa",
        "evento_at": "2026-06-15"
    }, headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["nome"] == "Clube Teste"
    assert data["id"] is not None


def test_list_clubes(client, auth_headers):
    client.post("/clubes", json={"nome": "C1"}, headers=auth_headers)
    client.post("/clubes", json={"nome": "C2"}, headers=auth_headers)

    resp = client.get("/clubes", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Old"}, headers=auth_headers)
    cid = create.json()["id"]

    resp = client.put(f"/clubes/{cid}", json={"nome": "New"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["nome"] == "New"


def test_delete_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "ToDelete"}, headers=auth_headers)
    cid = create.json()["id"]

    resp = client.delete(f"/clubes/{cid}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_clube_404(client, auth_headers):
    resp = client.delete("/clubes/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_ingressar_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Ingresso"}, headers=auth_headers)
    cid = create.json()["id"]

    resp = client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["clube_id"] == cid
    assert "inscrito_em" in data


def test_ingressar_duplicate_409(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Dup"}, headers=auth_headers)
    cid = create.json()["id"]

    client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    resp = client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    assert resp.status_code == 409


def test_ingressar_clube_inexistente_404(client, auth_headers):
    resp = client.post("/clubes/9999/ingressar", headers=auth_headers)
    assert resp.status_code == 404
```

### Executar Testes

```bash
cd api
pip install pytest httpx
pytest tests/ -v --tb=short
```

```
tests/test_auth.py::test_register_success          PASSED
tests/test_auth.py::test_register_duplicate         PASSED
tests/test_auth.py::test_login_returns_jwt          PASSED
tests/test_auth.py::test_login_wrong_password       PASSED
tests/test_auth.py::test_protected_route_no_token   PASSED
tests/test_clubes.py::test_create_clube             PASSED
tests/test_clubes.py::test_ingressar_clube          PASSED
tests/test_clubes.py::test_ingressar_duplicate_409  PASSED
...
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

---

## Architecture Decision Records (ADR)

### ADR-001: FastAPI em vez de Django REST / Flask

**Status:** Aceite  
**Contexto:** O sistema precisa de uma API REST com validação de schemas, documentação automática e suporte assíncrono. Django REST Framework traz overhead de um ORM opinado e admin desnecessário. Flask requer muitos plugins adicionais.  
**Decisão:** Usar FastAPI com Pydantic para validação e SQLAlchemy como ORM independente.  
**Consequências:**
- (+) Documentação OpenAPI gerada automaticamente (`/docs`)
- (+) Validação request/response via Pydantic com type hints nativos
- (+) Dependency injection nativo (`Depends()`) para DB sessions e auth
- (+) Performance superior (Starlette + Uvicorn ASGI)
- (−) Ecossistema mais pequeno que Django (menos packages prontos)
- (−) Sem admin panel built-in

### ADR-002: Argon2 em vez de bcrypt para hashing de passwords

**Status:** Aceite  
**Contexto:** O sistema armazena passwords de utilizadores. bcrypt é o standard de facto, mas tem limitações conhecidas (truncagem a 72 bytes, sem resistência a side-channel em GPUs).  
**Decisão:** Usar Argon2id via `passlib[argon2]` + `argon2_cffi`.  
**Consequências:**
- (+) Vencedor da Password Hashing Competition (2015) — resistente a GPU/ASIC/side-channel
- (+) Parâmetros configuráveis: memory cost, time cost, parallelism
- (+) `passlib.CryptContext` permite migração transparente de algoritmos (`deprecated="auto"`)
- (−) Requer `argon2_cffi` como dependência nativa (compilação C)
- (−) Ligeiramente mais lento que bcrypt por default (por design — é a feature)

### ADR-003: JWT stateless em vez de sessions server-side

**Status:** Aceite  
**Contexto:** A arquitetura é SPA + API separada. Sessions server-side requerem armazenamento partilhado (Redis/DB) e gestão de cookies cross-origin.  
**Decisão:** JWT (HMAC-SHA256) com payload `{sub, id, tipo_id, exp}`, tempo de vida 30 minutos, sem refresh token.  
**Consequências:**
- (+) Stateless — o servidor não guarda estado de sessão, escala horizontalmente
- (+) Frontend guarda token em `localStorage`, envia via `Authorization: Bearer`
- (+) Payload contém `tipo_id` → controlo de acesso sem query adicional à BD
- (−) Token não revogável antes do `exp` (sem blacklist implementada)
- (−) `localStorage` vulnerável a XSS (mitigado pela ausência de inputs não sanitizados em páginas autenticadas)
- (−) Sem refresh token — utilizador precisa re-login após 30 min

**Trade-off aceite:** Para o scope do projeto, a simplicidade compensa a ausência de revogação. Uma evolução futura pode adicionar refresh tokens + blacklist em Redis.

### ADR-004: UniqueConstraint na tabela de inscrição (membro_clube)

**Status:** Aceite  
**Contexto:** Utilizadores podem inscrever-se em clubes. Sem constraint, o mesmo utilizador pode inscrever-se N vezes no mesmo clube (bugs de UI, double-click, replay de requests).  
**Decisão:** `UniqueConstraint("utilizador_id", "clube_id")` a nível de BD + catch de `IntegrityError` na API com rollback e HTTP 409.  
**Consequências:**
- (+) Integridade garantida a nível de BD — impossível bypass via SQL direto ou race conditions
- (+) A API trata o erro graciosamente com mensagem localizada
- (+) Mais robusto que validação apenas em application layer (que sofre de TOCTOU)
- (−) Requer `try/except IntegrityError` + `db.rollback()` explícito no endpoint

```python
# Implementação do padrão
try:
    db.commit()
except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail=f"Já está inscrito no clube '{clube.nome}'")
```

### ADR-005: SSR (Nuxt) com `<ClientOnly>` para componentes DOM-dependent

**Status:** Aceite  
**Contexto:** O Nuxt 4 usa SSR por default para SEO e performance. Mas bibliotecas como FullCalendar e Leaflet manipulam o DOM diretamente e falham em ambiente Node.js (sem `window`/`document`).  
**Decisão:** Usar `<ClientOnly>` wrapper do Nuxt para componentes incompatíveis com SSR, com skeleton de fallback.  
**Consequências:**
- (+) SSR funciona para páginas estáticas (index, aboutus, login) — melhor First Contentful Paint
- (+) Componentes client-only (calendar, maps) renderizam apenas no browser
- (+) Skeleton mantém layout estável durante hidratação (evita CLS)
- (−) Conteúdo client-only invisível para crawlers sem JavaScript
- (−) Ligeiro flash durante hidratação em conexões lentas

### ADR-006: CORS `allow_origins=["*"]` em desenvolvimento

**Status:** Aceite (temporário)  
**Contexto:** Frontend e backend correm em portas diferentes (3000 vs 8000). Sem CORS, o browser bloqueia pedidos cross-origin.  
**Decisão:** `allow_origins=["*"]` com `allow_credentials=False` para desenvolvimento.  
**Consequências:**
- (+) Desenvolvimento sem friction entre frontend e backend
- (−) Em produção, deve ser restrito ao domínio do frontend
- (−) `allow_credentials=False` impede uso de cookies (irrelevante — usamos JWT em header)

> **TODO produção:** Alterar para `allow_origins=["https://domain.com"]`.

### ADR-007: Monólito modular em vez de microserviços

**Status:** Aceite  
**Contexto:** O projeto é desenvolvido solo. A complexidade operacional de microserviços (deploy, networking, service discovery) não se justifica.  
**Decisão:** Monólito com separação clara em módulos (`main.py`, `auth.py`, `models.py`, `database.py`) e repositório único (monorepo).  
**Consequências:**
- (+) Deploy simples — um processo `uvicorn` serve toda a API
- (+) Sem latência de rede entre serviços
- (+) Refactoring fácil — tudo no mesmo codebase
- (+) Frontend e backend no mesmo repo — versionamento conjunto
- (−) Escalabilidade limitada a vertical (mitigado pelo ASGI Uvicorn com workers)
- (−) Se o projeto crescer significativamente, pode precisar de decomposição

---

## Estrutura do Projeto

```
-Manueli-s-Clubes/
├── README.md
├── EXPLICACAO.md
├── package.json                     # deps globais (Bootstrap, Chart.js, Leaflet)
│
├── api/                             # Backend (FastAPI)
│   ├── main.py                      # App factory, CRUD routes, stats, inscrições
│   ├── auth.py                      # Router /auth, JWT, Argon2
│   ├── models.py                    # ORM models + Pydantic schemas
│   ├── database.py                  # Engine, SessionLocal, get_db(), init_db()
│   ├── requirements.txt
│   └── tests/                       # pytest + httpx
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_clubes.py
│       ├── test_utilizadores.py
│       ├── test_tipouser.py
│       ├── test_mapas.py
│       └── test_stats.py
│
└── nuxt-app/                        # Frontend (Nuxt 4)
    ├── nuxt.config.js
    ├── package.json
    ├── tsconfig.json
    ├── components/
    │   └── Header.vue               # Nav global
    ├── pages/
    │   ├── index.vue                # Landing (SSR) — stats públicas
    │   ├── login.vue                # Auth — FormData → /auth/token
    │   ├── dashboard.vue            # KPIs + Chart.js (line + doughnut)
    │   ├── clubes.vue               # CRUD table + permissões por tipo_id
    │   ├── mapas.vue                # Leaflet <ClientOnly> + CRUD pontos
    │   ├── calendario.vue           # FullCalendar <ClientOnly> + ingressar
    │   ├── chat.vue                 # Chat
    │   └── aboutus.vue              # Sobre nós — stats em tempo real
    ├── assets/{css,js,images}/      # Bootstrap 5 (source + minified)
    └── public/robots.txt
```

---

## Setup

### Variáveis de Ambiente (`api/.env`)

```env
MYSQL_HOST=localhost
MYSQL_PORT=5432
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_DATABASE=clubes_db
SECRET_KEY=<random-256-bit-hex>
ALGORITHM=HS256
```

### Backend

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# → http://localhost:8000/docs (Swagger UI)
```

### Frontend

```bash
cd nuxt-app
npm install
npm run dev
# → http://localhost:3000
```

---

## Autor

**Manuel Silvestre**
