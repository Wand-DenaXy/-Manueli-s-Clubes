# Revisão do CV — Backend e Full-Stack

Baseado nas imagens dos 4 CVs enviados: backend EN, backend PT, full-stack EN e full-stack PT.

---

## Nota de Venda

### CV Backend — atual

- `7.5/10`

### CV Full-Stack — atual

- `7/10`

### Como te estás a vender no geral — atual

- `7/10`

### Potencial com a versão corrigida abaixo

- Backend: `8.5/10`
- Full-Stack: `8/10`

---

## O Que Está Forte No Teu CV

- O layout está limpo e legível.
- O projeto principal está logo no topo, o que é a decisão certa.
- A experiência na Arrow4D ajuda a provar que não tens só projetos de escola.
- Já usas linguagem de entrega real: multi-tenant, Stripe, RBAC, JWT, Redis, Celery.
- O CV passa imagem de alguém que constrói software completo e não apenas exercícios.

---

## O Que Está A Baixar A Força Do CV

- Estás a usar métricas desatualizadas no projeto: `93% coverage`, `CI/CD` e `Nuxt 3` já não estão alinhados com o estado atual do repo.
- O projeto é vendido demasiado como lista de tecnologias e pouco como problema resolvido.
- Algumas bullets são redundantes entre si.
- O CV backend ainda está demasiado aberto em skills; PHP, Laravel, Kotlin e Flutter diluem foco se a vaga for Python backend.
- O CV full-stack também pode ser mais forte se o projeto destacar mais os fluxos completos de produto: dashboard, calendário, mapas, pagamentos e notificações.
- Frases como `reducing load` ou `improving API performance` são boas, mas sem métrica concreta convém suavizar a formulação.

---

## Correções Obrigatórias No Projeto

Estas tens mesmo de corrigir no CV antes de enviar:

- `93% coverage` → `84% coverage`
- `CI/CD` → `CI`
- `Nuxt 3` → `Nuxt 4`
- `Docker build` → `API Docker build` se queres ser 100% rigoroso com o workflow atual

---

## Recomendação de Posicionamento

### Para CV Backend

O teu foco deve ser:

- arquitetura backend
- Stripe + webhooks + Celery
- Redis cache + rate limiting
- testes + CI
- multi-tenancy + RBAC

### Para CV Full-Stack

O teu foco deve ser:

- ownership end-to-end
- frontend + backend + pagamentos
- dashboard + mapas + calendário + subscriptions
- produto real e integração entre camadas

---

## Ajuste Recomendado Nas Skills

### Backend CV — skills recomendadas

**Back-End:** Python · FastAPI · SQLAlchemy · PostgreSQL · Redis · Celery · Stripe · JWT  
**Front-End:** Nuxt · Vue 3 · JavaScript · Bootstrap  
**Tools:** Docker · GitHub Actions · pytest · ruff · Git  
**Languages:** Portuguese (Native) · English (B1) · Spanish (A2)

### Full-Stack CV — skills recomendadas

**Front-End:** Nuxt · Vue 3 · JavaScript · Bootstrap · HTML/CSS  
**Back-End:** Python · FastAPI · SQLAlchemy · PostgreSQL · Redis · Celery · Stripe · JWT  
**Tools:** Docker · GitHub Actions · pytest · ruff · Git  
**Languages:** Portuguese (Native) · English (B1) · Spanish (A2)

Se quiseres manter Laravel/PHP/MySQL, coloca-os depois dos stacks principais ou usa um bloco `Additional`.

---

## Texto Final — Backend EN

### Role line

`[Back-End]`

### Manueli's Clubes — replacement bullets

- Built a **multi-tenant SaaS platform** with **RBAC (3 roles)**, organization-based data isolation, JWT authentication, and subscription plan limits.
- Implemented **recurring payments with Stripe Checkout** and **asynchronous webhook processing with Celery + Redis**, including retries and idempotency.
- Designed and shipped a **FastAPI backend with 34 REST endpoints**, covering auth, CRUD, stats, memberships, payments, notifications, and webhooks.
- Added **Redis caching and per-IP rate limiting**, including TTL-based caching and prefix invalidation for critical endpoints.
- Structured the project with **72 automated tests, 84% coverage, and CI quality gates** for tests, linting, and API Docker build validation.

### Short one-line version

Built a backend-heavy SaaS for club management with FastAPI, PostgreSQL, Redis, Celery, Stripe, JWT, RBAC, multi-tenancy, 34 REST endpoints, and 72 automated tests.

---

## Texto Final — Backend PT

### Linha de role

`[Back-End]`

### Manueli's Clubes — bullets para substituir

- Desenvolvi uma **plataforma SaaS multi-tenant** com **RBAC (3 perfis)**, isolamento de dados por organização, autenticação JWT e limites por plano.
- Implementei **pagamentos recorrentes com Stripe Checkout** e **processamento assíncrono de webhooks com Celery + Redis**, incluindo retries e idempotência.
- Estruturei um **backend em FastAPI com 34 endpoints REST**, cobrindo autenticação, CRUD, estatísticas, memberships, pagamentos, notificações e webhooks.
- Adicionei **cache Redis e rate limiting por IP**, com TTL e invalidação por prefixo para endpoints críticos.
- Garanti qualidade com **72 testes automatizados, 84% de cobertura e CI** com validação de testes, lint e build Docker da API.

### Versão curta de uma linha

Desenvolvi um backend SaaS para gestão de clubes com FastAPI, PostgreSQL, Redis, Celery, Stripe, JWT, RBAC, multi-tenancy, 34 endpoints REST e 72 testes automatizados.

---

## Texto Final — Full-Stack EN

### Role line

`[Full-Stack]`

### Manueli's Clubes — replacement bullets

- Built an **end-to-end SaaS platform** for club management with **Nuxt/Vue on the frontend** and **FastAPI on the backend**.
- Delivered full product flows including **JWT authentication, RBAC, multi-tenancy, dashboard analytics, interactive maps, club calendar, and subscription plans**.
- Integrated **Stripe recurring payments** with **asynchronous webhook processing using Celery + Redis**, including retries, idempotency, notifications, and transactional emails.
- Designed a backend with **34 REST endpoints**, plus Redis caching, rate limiting, and Docker Compose orchestration across 5 services.
- Structured the project with **72 automated tests, 84% coverage, and CI quality gates** for tests, linting, and API Docker build validation.

### Short one-line version

Built a full-stack SaaS for club management with Nuxt/Vue, FastAPI, PostgreSQL, Redis, Stripe, Celery, dashboard analytics, maps, subscriptions, and 72 automated tests.

---

## Texto Final — Full-Stack PT

### Linha de role

`[Full-Stack]`

### Manueli's Clubes — bullets para substituir

- Desenvolvi uma **plataforma SaaS end-to-end** para gestão de clubes com **Nuxt/Vue no frontend** e **FastAPI no backend**.
- Entreguei fluxos completos de produto com **autenticação JWT, RBAC, multi-tenancy, dashboard com métricas, mapas interativos, calendário de clubes e planos de subscrição**.
- Integrei **pagamentos recorrentes com Stripe** e **processamento assíncrono de webhooks com Celery + Redis**, incluindo retries, idempotência, notificações e emails transacionais.
- Estruturei o backend com **34 endpoints REST**, cache Redis, rate limiting e orquestração com Docker Compose em 5 serviços.
- Garanti qualidade com **72 testes automatizados, 84% de cobertura e CI** com validação de testes, lint e build Docker da API.

### Versão curta de uma linha

Desenvolvi um SaaS full-stack para gestão de clubes com Nuxt/Vue, FastAPI, PostgreSQL, Redis, Stripe, Celery, dashboard, mapas, subscrições e 72 testes automatizados.

---

## O Que Eu Mudaria No CV Além Do Projeto

### Header

Se quiseres vender melhor, o teu headline pode ser um pouco mais orientado ao mercado.

### Backend

`Backend Developer | Python, FastAPI, APIs, Stripe, Celery, Redis`

### Full-Stack

`Full-Stack Developer | Nuxt, Vue, FastAPI, PostgreSQL, Redis`

---

## Arrow4D — Ajuste Recomendado

Esta experiência está boa, mas também a podes vender com mais força.

### EN

- Built a B2C full-stack platform from scratch with **FastAPI + Nuxt**, delivering **4 role-specific dashboards** and production usage with real clients.
- Architected a **40+ endpoint REST API** with FastAPI, SQLAlchemy, and PostgreSQL, organised by domain for maintainability and scale.
- Implemented **JWT + RBAC** with full permission isolation across 4 user profiles.
- Automated the rental lifecycle with persistent cart and integrated billing, replacing a fully manual process.

### PT

- Desenvolvi de raiz uma plataforma B2C full-stack com **FastAPI + Nuxt**, com **4 dashboards por perfil** e utilização real em produção.
- Estruturei uma **API REST com 40+ endpoints** em FastAPI, SQLAlchemy e PostgreSQL, organizada por domínio para facilitar manutenção e escala.
- Implementei **JWT + RBAC** com separação total de permissões entre 4 perfis.
- Automatizei o ciclo de aluguer com carrinho persistente e faturação integrada, substituindo um processo totalmente manual.

---

## Recomendação Final

### Se fores enviar para vagas Backend

- usa a versão backend
- reduz ruído de frontend nas skills
- mantém Manueli's Clubes como primeiro projeto
- deixa Arrow4D logo a seguir para provar experiência real

### Se fores enviar para vagas Full-Stack

- usa a versão full-stack
- mantém mapas, dashboard, calendário e Stripe no texto
- mostra ownership completo de produto

---

## Resposta Direta À Tua Pergunta

Sim, estás a vender-te **bem acima da média**, mas ainda **abaixo do que este projeto te permite vender**.

Hoje:

- projeto: `8/10`
- CV atual: `7/10`
- potencial com os textos acima: `8.5/10`

Se corrigires o texto do projeto, atualizares as métricas e afinares o foco entre backend e full-stack, o teu CV fica claramente mais forte.
