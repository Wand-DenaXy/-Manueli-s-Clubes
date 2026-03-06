# Manueli's Clubes – Documentação do Projeto

Uma aplicação web full-stack para gestão de clubes, desenvolvida com **Nuxt 4 (Vue 3)** no frontend e **FastAPI (Python)** no backend, com autenticação JWT, inscrição em clubes, mapas interativos, dashboard com gráficos e calendário.

<img width="1000" height="500" alt="ManueliClube" src="https://github.com/user-attachments/assets/786aee57-cdbc-4be2-823b-51c221d7e4b8" />

---

## Descrição do Projeto

**Manueli's Clubes** é uma plataforma web que permite a criação, edição, listagem e remoção de clubes, gestão de utilizadores com diferentes níveis de acesso, inscrição de membros em clubes, visualização de localizações em mapas interativos, e consulta de estatísticas através de um dashboard dinâmico.

O projeto foi desenvolvido com foco em:
- Arquitetura **API REST** com separação clara entre frontend e backend
- Autenticação e autorização com **JWT (JSON Web Tokens)**
- Operações **CRUD assíncronas** via `fetch` API
- Sistema de **inscrição em clubes** com controlo de duplicação
- Interface moderna, responsiva e com tema **dark**

---

## Principais Funcionalidades

- **Autenticação & Autorização** — Sistema de login com tokens JWT, suporte a diferentes tipos de utilizador (admin, gestor, etc.) e hashing de passwords com Argon2
- **Gestão de Clubes** — CRUD completo de clubes (nome, email, telefone, localidade, data de evento) com controlo de permissões por tipo de utilizador
- **Inscrição em Clubes** — Utilizadores podem ingressar em clubes através do calendário, com prevenção de inscrições duplicadas via constraint única na BD
- **Gestão de Utilizadores** — Registo, listagem, edição e remoção de utilizadores com tipos de acesso configuráveis
- **Dashboard com Estatísticas** — Painel com KPIs, gráfico de crescimento de utilizadores ao longo do ano e distribuição por categorias (Chart.js)
- **Mapas Interativos** — Visualização geográfica dos clubes com Leaflet, criação de pontos no mapa associados a clubes
- **Calendário de Clubes** — Visualização de clubes num calendário interativo (FullCalendar) com modal de detalhes e inscrição direta
- **Página "Sobre Nós"** — Apresentação da missão, valores e equipa, com estatísticas em tempo real

---

## Tech Stack

| Componente          | Tecnologia         | Detalhes                                              |
|---------------------|--------------------|-------------------------------------------------------|
| Frontend Framework  | Nuxt 4 (Vue 3)    | SSR, routing automático, componentes `.vue`            |
| Backend Framework   | FastAPI (Python)   | API REST com documentação automática (`/docs`)         |
| Base de Dados       | PostgreSQL         | Via SQLAlchemy ORM + psycopg2                          |
| Autenticação        | JWT                | python-jose + OAuth2PasswordBearer                     |
| Hashing de Passwords| Argon2             | Via passlib com argon2_cffi                             |
| Mapas               | Leaflet.js         | Mapas interativos com marcadores por clube             |
| Gráficos            | Chart.js           | Gráficos de linha e doughnut no dashboard              |
| Calendário          | FullCalendar       | Calendário interativo com plugins dayGrid e interaction |
| Alertas             | SweetAlert2        | Feedback visual ao utilizador                          |
| CSS Framework       | Bootstrap 5        | Layout e componentes visuais base                      |
| Variáveis de Ambiente| python-dotenv     | Configuração da BD e API Keys via `.env`               |

### Requisitos de Sistema

**Backend:**
- Python 3.10+
- PostgreSQL
- Dependências em `api/requirements.txt`

**Frontend:**
- Node.js 18+
- npm ou yarn
- Dependências em `nuxt-app/package.json`

---

## Arquitetura Geral

```
┌──────────────────────────────────┐
│           Frontend               │
│     Nuxt 4 (Vue 3 + SSR)        │
│  Pages, Components, Leaflet,    │
│  Chart.js, FullCalendar          │
└──────────────┬───────────────────┘
               │  fetch (HTTP/JSON)
               │  Authorization: Bearer <JWT>
               ▼
┌──────────────────────────────────┐
│           Backend API            │
│    FastAPI (Python) :8000        │
│  Rotas REST + Auth + Inscrições  │
└──────────────┬───────────────────┘
               │  SQLAlchemy ORM
               ▼
┌──────────────────────────────────┐
│        Base de Dados             │
│     PostgreSQL (psycopg2)        │
│  Tabelas: clubes, utilizador,   │
│  tipouser, mapas, membro_clube  │
└──────────────────────────────────┘
```

---

## Estrutura do Projeto

```
-Manueli-s-Clubes/
├── README.md                         # Documentação do projeto
├── EXPLICACAO.md                     # Explicação técnica detalhada
├── package.json                      # Dependências globais (Bootstrap, Chart.js, Leaflet, etc.)
│
├── api/                              # Backend — API REST (FastAPI)
│   ├── main.py                       # Entry point da API, rotas CRUD, inscrições e estatísticas
│   ├── auth.py                       # Autenticação JWT, registo e login de utilizadores
│   ├── models.py                     # Modelos SQLAlchemy (ORM) e schemas Pydantic
│   ├── database.py                   # Configuração da ligação à BD (PostgreSQL via SQLAlchemy)
│   └── requirements.txt              # Dependências Python do backend
│
└── nuxt-app/                         # Frontend — Aplicação Nuxt 4 (Vue 3)
    ├── nuxt.config.js                # Configuração do Nuxt (CSS, devtools)
    ├── package.json                  # Dependências Node.js do frontend
    ├── tsconfig.json                 # Configuração TypeScript
    │
    ├── components/
    │   └── Header.vue                # Componente de navegação global (logo + links)
    │
    ├── pages/
    │   ├── index.vue                 # Página inicial — hero, estatísticas públicas, CTA
    │   ├── login.vue                 # Página de autenticação — login com tipo de utilizador
    │   ├── dashboard.vue             # Dashboard — KPIs, gráficos de utilizadores e categorias
    │   ├── clubes.vue                # Gestão de clubes — formulário + tabela CRUD
    │   ├── mapas.vue                 # Mapas — visualização Leaflet, pontos por clube
    │   ├── calendario.vue            # Calendário — FullCalendar com inscrição em clubes
    │   ├── chat.vue                  # Página de chat da plataforma
    │   └── aboutus.vue               # Sobre nós — missão, valores, equipa, estatísticas
    │
    ├── assets/
    │   ├── css/
    │   │   ├── bootstrap.css         # Estilos Bootstrap (fonte)
    │   │   └── bootstrap.min.css     # Estilos Bootstrap (minificado)
    │   ├── js/
    │   │   ├── bootstrap.js          # JavaScript Bootstrap (fonte)
    │   │   └── bootstrap.min.js      # JavaScript Bootstrap (minificado)
    │   └── images/                   # Imagens do projeto
    │
    └── public/
        └── robots.txt                # Configuração para crawlers
```

---

## Descrição Detalhada de Cada Ficheiro

### API (Backend)

| Ficheiro         | Propósito                                                                                                                                   |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `main.py`        | Entry point da API FastAPI. Define todas as rotas CRUD para clubes, utilizadores, tipos de utilizador e mapas. Inclui endpoint de inscrição em clubes (`POST /clubes/{id}/ingressar`), endpoints de estatísticas (`/stats`, `/statstpuser`, `/registrations`). Configura CORS e inicializa a BD no startup. |
| `auth.py`        | Módulo de autenticação. Implementa registo (`POST /auth/`), login com geração de token JWT (`POST /auth/token`), verificação de passwords com Argon2, e middleware `get_current_user` para proteger rotas. |
| `models.py`      | Define os modelos ORM SQLAlchemy (`ClubeModel`, `UtilizadorModel`, `TipoUserModel`, `MapaModel`, `MembroClubeModel`) e os schemas Pydantic para validação de entrada/saída (`ClubeCreate`, `ClubeResponse`, `IngressarResponse`, etc.). Inclui relações entre tabelas (clube↔mapas, clube↔membros, tipo↔utilizadores, utilizador↔clubes_inscritos). |
| `database.py`    | Configuração da ligação à BD PostgreSQL via SQLAlchemy. Lê credenciais de variáveis de ambiente (`.env`). Fornece o dependency `get_db()` para injeção de sessão nas rotas e `init_db()` para criação automática de tabelas. |
| `requirements.txt` | Lista de dependências Python: FastAPI, Uvicorn, SQLAlchemy, psycopg2, passlib, python-jose, argon2_cffi, etc. |

### Frontend (Nuxt / Vue)

| Ficheiro          | Propósito                                                                                                                                             |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Header.vue`      | Componente reutilizável de navegação. Exibe logo "Manueli's Clubes", link "Sobre nós" e botão "Entrar". Usado nas páginas públicas (index, aboutus). |
| `index.vue`       | Landing page pública. Apresenta hero com mensagem de boas-vindas, botões de ação, e estatísticas em tempo real (clubes, membros, localizações) obtidas da API `/stats`. |
| `login.vue`       | Página de autenticação. Formulário com username, password e seleção de tipo de utilizador (carregado da API). Envia credenciais via `FormData` para `/auth/token` e guarda o JWT no `localStorage`. |
| `dashboard.vue`   | Painel de controlo protegido. Exibe KPIs (total clubes, membros, tipos), gráfico de linha de registos por mês (`/registrations`) e gráfico doughnut de distribuição por tipo (`/statstpuser`). Requer autenticação via JWT. |
| `clubes.vue`      | Página de gestão de clubes. Formulário para criar novos clubes (com campo de data de evento) e tabela com edição inline. Operações de guardar e apagar com confirmação via SweetAlert2. Controlo de permissões: apenas admins (tipo_id=1) podem editar/apagar. |
| `mapas.vue`       | Página de mapas interativos com Leaflet. Painel lateral com lista de clubes e pontos. Permite adicionar novos pontos no mapa (clique no mapa ou coordenadas manuais), associados a clubes. Controlo de acesso para admins e gestores. |
| `calendario.vue`  | Calendário com FullCalendar. Cada clube aparece como evento na sua data. Modal de detalhe permite inscrever-se num clube via `POST /clubes/{id}/ingressar`. Usa `<ClientOnly>` para compatibilidade com SSR do Nuxt. |
| `chat.vue`        | Página de chat da plataforma. |
| `aboutus.vue`     | Página "Sobre nós". Apresenta missão, valores (Comunidade, Autenticidade, Abertura, Movimento), equipa (Manueli Silvestre — Fundador & CEO) e CTA para registo. Carrega estatísticas em tempo real. |

---

## Modelo de Dados

```
┌─────────────────┐       ┌─────────────────┐
│    tipouser     │       │   utilizador    │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────│ tipo_id (FK)    │
│ descricao       │  1:N  │ id (PK)         │
└─────────────────┘       │ username        │
                          │ password        │
                          │ created_at      │
                          └────────┬────────┘
                                   │
                                   │ 1:N
                                   ▼
                          ┌─────────────────┐
                          │  membro_clube   │
                          ├─────────────────┤
                          │ id (PK)         │
                          │ utilizador_id(FK)│
                          │ clube_id (FK)   │
                          │ inscrito_em     │
                          │ UQ(util,clube)  │
                          └────────┬────────┘
                                   │
                                   │ N:1
                                   ▼
┌─────────────────┐       ┌─────────────────┐
│     mapas       │       │     clubes      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ descricao       │──────►│ nome            │
│ latitude        │  N:1  │ email           │
│ longitude       │       │ telefone        │
│ clube_id (FK)   │       │ localidade      │
└─────────────────┘       │ evento_at       │
                          │ created_at      │
                          └─────────────────┘
```

---

## Endpoints da API

### Autenticação (`/auth`)

| Método | Rota           | Descrição                        | Autenticação |
|--------|----------------|----------------------------------|--------------|
| POST   | `/auth/`       | Registo de novo utilizador       | Não          |
| POST   | `/auth/token`  | Login — devolve JWT              | Não          |

### Clubes (`/clubes`)

| Método | Rota                          | Descrição                        | Autenticação |
|--------|-------------------------------|----------------------------------|--------------|
| POST   | `/clubes`                     | Criar novo clube                 | JWT          |
| GET    | `/clubes`                     | Listar todos os clubes           | JWT          |
| PUT    | `/clubes/{id}`                | Atualizar clube                  | JWT          |
| DELETE | `/clubes/{id}`                | Apagar clube                     | JWT          |
| POST   | `/clubes/{id}/ingressar`      | Inscrever-se num clube           | JWT          |

### Utilizadores (`/utilizadores`)

| Método | Rota                    | Descrição                   | Autenticação |
|--------|-------------------------|-----------------------------|--------------|
| GET    | `/utilizadores`         | Listar utilizadores         | JWT          |
| PUT    | `/utilizadores/{id}`    | Atualizar utilizador        | JWT          |
| DELETE | `/utilizadores/{id}`    | Apagar utilizador           | JWT          |

### Tipos de Utilizador (`/tipouser`)

| Método | Rota               | Descrição                    | Autenticação |
|--------|---------------------|------------------------------|--------------|
| POST   | `/tipouser`         | Criar tipo de utilizador     | JWT          |
| GET    | `/tipouser`         | Listar tipos                 | Não          |
| PUT    | `/tipouser/{id}`    | Atualizar tipo               | JWT          |
| DELETE | `/tipouser/{id}`    | Apagar tipo                  | JWT          |

### Mapas (`/mapas`)

| Método | Rota             | Descrição              | Autenticação |
|--------|-------------------|------------------------|--------------|
| POST   | `/mapas`          | Criar ponto no mapa    | JWT          |
| GET    | `/mapas`          | Listar pontos          | JWT          |
| PUT    | `/mapas/{id}`     | Atualizar ponto        | JWT          |
| DELETE | `/mapas/{id}`     | Apagar ponto           | JWT          |

### Estatísticas

| Método | Rota              | Descrição                                     | Autenticação |
|--------|--------------------|-----------------------------------------------|--------------|
| GET    | `/stats`           | Totais gerais (clubes, utilizadores, etc.)    | Não          |
| GET    | `/statstpuser`     | Distribuição de utilizadores por tipo         | JWT          |
| GET    | `/registrations`   | Registos de utilizadores por mês (ano atual)  | JWT          |

---

## Fluxo de Autenticação

```
Cliente                              API FastAPI
  │                                      │
  ├─ Preenche username, password,        │
  │  tipo de utilizador                  │
  │                                      │
  ├─ POST /auth/token ──────────────────►│
  │  (FormData: username, password,      │
  │   tipo_id)                           ├─ Busca utilizador na BD
  │                                      ├─ Verifica password (Argon2)
  │                                      ├─ Verifica tipo_id
  │                                      ├─ Gera JWT (30 min)
  │◄───── { access_token, bearer } ──────┤
  │                                      │
  ├─ Guarda token no localStorage        │
  ├─ Redireciona para /dashboard         │
  │                                      │
  ├─ GET /clubes ───────────────────────►│
  │  Header: Authorization: Bearer <JWT> │
  │                                      ├─ Valida JWT
  │                                      ├─ Extrai user do token
  │◄───── [ lista de clubes ] ───────────┤
```

---

## Fluxo CRUD de Clubes

```
Utilizador                 Frontend (Vue)              API (FastAPI)           PostgreSQL
  │                            │                            │                      │
  ├─ Preenche formulário       │                            │                      │
  ├─ Clica "Criar Clube" ────►│                            │                      │
  │                            ├─ POST /clubes ────────────►│                      │
  │                            │  { nome, email, tel, loc,  ├─ Valida JWT          │
  │                            │    evento_at }             ├─ INSERT INTO clubes ─►│
  │                            │                            │◄─ clube criado ───────┤
  │                            │◄─── ClubeResponse ─────────┤                      │
  │◄── SweetAlert "Sucesso!" ──┤                            │                      │
  │                            ├─ GET /clubes ─────────────►│                      │
  │                            │                            ├─ SELECT * FROM clubes►│
  │                            │◄─── [ clubes ] ────────────┤◄─────────────────────┤
  │◄── Tabela atualizada ──────┤                            │                      │
```

---

## Fluxo de Inscrição em Clube

```
Utilizador                 Calendário (Vue)            API (FastAPI)           PostgreSQL
  │                            │                            │                      │
  ├─ Clica num evento ────────►│                            │                      │
  │                            ├─ Abre modal de detalhe     │                      │
  │                            │  (nome, email, tel, loc)   │                      │
  │                            │                            │                      │
  ├─ Clica "Ingressar" ──────►│                            │                      │
  │                            ├─ POST /clubes/{id}/        │                      │
  │                            │  ingressar ───────────────►│                      │
  │                            │                            ├─ Valida JWT          │
  │                            │                            ├─ Verifica se clube   │
  │                            │                            │  existe              │
  │                            │                            ├─ INSERT membro_clube─►│
  │                            │                            │  (UQ constraint)     │
  │                            │                            │◄─ inscrito ───────────┤
  │                            │◄─── IngressarResponse ─────┤                      │
  │◄── "Inscrito com sucesso!" ┤                            │                      │
```

---

## Como Executar

### 1. Configurar a Base de Dados

Criar um ficheiro `.env` na pasta `api/` com as credenciais do PostgreSQL:

```env
MYSQL_HOST=localhost
MYSQL_PORT=5432
MYSQL_USER=seu_user
MYSQL_PASSWORD=sua_password
MYSQL_DATABASE=clubes_db
```

### 2. Instalar e Executar o Backend (Terminal 1)

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Saída esperada:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

A documentação interativa da API fica disponível em: `http://localhost:8000/docs`

### 3. Instalar e Executar o Frontend (Terminal 2)

```bash
cd nuxt-app
npm install
npm run dev
```

Saída esperada:
```
Nuxt 4.x with Nitro
Local:    http://localhost:3000/
```

### 4. Utilização

1. Aceder a `http://localhost:3000` — Página inicial pública
2. Clicar em **"Entrar"** — Redireciona para a página de login
3. Criar conta via API (`POST /auth/`) ou usar credenciais existentes
4. Após login, é redirecionado para o **Dashboard**
5. Navegar pela sidebar: **Clubes**, **Mapas**, **Calendário**
6. No **Calendário**, clicar num clube e **"Ingressar"** para se inscrever

---

## Principais Decisões Técnicas

### Utilização de FastAPI + SQLAlchemy

**Justificação:**
- API REST de alta performance com documentação automática (Swagger UI)
- ORM que permite trabalhar com objetos Python em vez de SQL puro
- Validação automática de dados via Pydantic

### Autenticação com JWT + Argon2

**Justificação:**
- Tokens JWT permitem autenticação stateless e escalável
- Argon2 é o algoritmo de hashing vencedor da Password Hashing Competition, mais seguro que bcrypt
- Diferentes tipos de utilizador permitem controlo de acesso granular

### Tabela de Inscrição (membro_clube) com UniqueConstraint

**Justificação:**
- Relação muitos-para-muitos entre utilizadores e clubes
- `UniqueConstraint("utilizador_id", "clube_id")` impede inscrições duplicadas a nível de BD
- `IntegrityError` tratado na API para devolver resposta amigável (HTTP 409)

### Nuxt 4 com SSR

**Justificação:**
- Server-Side Rendering para melhor SEO e performance inicial
- Routing automático baseado em ficheiros (`pages/`)
- Ecossistema Vue 3 com Composition API (`<script setup>`)

### Utilização de `<ClientOnly>` no Calendário

**Justificação:**
- O FullCalendar manipula o DOM diretamente, incompatível com SSR
- `<ClientOnly>` garante que o componente só é renderizado no browser
- Skeleton de fallback mantém a experiência visual durante o carregamento

### Operações CRUD via Fetch API

**Justificação:**
- Comunicação assíncrona sem recarregamento de página
- Feedback visual imediato ao utilizador via SweetAlert2
- Headers de autorização enviados em cada pedido protegido

---

## Autor

**Manuel Silvestre**
