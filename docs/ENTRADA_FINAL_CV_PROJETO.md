# Entrada Final CV — Manueli's Clubes

Este ficheiro contém versões **prontas a colar no CV** para vender o projeto melhor.

Regra de uso:

- usa a versão **Backend** quando quiseres puxar mais por API, integrações, arquitetura e processamento assíncrono
- usa a versão **Full-Stack** quando quiseres vender ownership end-to-end
- não uses as duas ao mesmo tempo no mesmo CV; escolhe a que melhor serve a vaga

---

## Versão 1 — Backend

### Título do projeto

**Manueli's Clubes — Backend-heavy SaaS com pagamentos, webhooks e multi-tenancy**

### Subtítulo curto

FastAPI · PostgreSQL · Redis · Celery · Stripe · JWT · RBAC · Docker · CI

### Versão curta para secção de projetos

Desenvolvi o backend de um SaaS para gestão de clubes com autenticação JWT, RBAC, multi-tenancy por organização, pagamentos recorrentes com Stripe, processamento assíncrono de webhooks com Celery, cache Redis e rate limiting. O projeto inclui 34 endpoints REST, 72 testes automatizados, 84% de cobertura e pipeline de CI com testes, lint e build da imagem Docker da API.

### Versão final pronta a colar no CV — 3 bullets

- Desenvolvi um backend em **FastAPI** para um SaaS de gestão de clubes, com **34 endpoints REST**, autenticação **JWT**, **RBAC** por perfil e **multi-tenancy** por organização.
- Implementei **pagamentos recorrentes com Stripe Checkout** e **processamento assíncrono de webhooks com Celery**, incluindo **idempotência, retries, notificações e emails transacionais**.
- Estruturei a aplicação com **PostgreSQL, Redis, rate limiting, cache com invalidação por prefixo, 72 testes automatizados, 84% de cobertura** e **CI** com validação de testes, lint e build Docker da API.

### Versão mais forte para vagas backend

- Construí o backend de uma plataforma SaaS orientada a multi-tenancy com **JWT, RBAC, limites por plano e isolamento por organização**, cobrindo autenticação, CRUD, estatísticas, memberships e notificações.
- Modelei e implementei fluxos de pagamento reais com **Stripe**, incluindo criação de sessão de checkout, validação de webhook, **idempotência por event_id** e processamento assíncrono com **Celery + Redis**.
- Garanti qualidade técnica com **72 testes**, **84% coverage**, quality gates em CI, cache Redis com TTL/invalidação, e documentação técnica detalhada de arquitetura, modelo de dados e fluxos críticos.

### Stack a colocar no CV

**FastAPI, Python, SQLAlchemy, PostgreSQL, Redis, Celery, Stripe, JWT, Argon2, Docker Compose, GitHub Actions, pytest, ruff**

### Quando esta versão é melhor

- vagas de backend Python
- vagas de APIs e integrações
- vagas com foco em arquitetura aplicacional
- vagas com Stripe, filas, webhooks, Redis ou micro-serviços leves

---

## Versão 2 — Full-Stack

### Título do projeto

**Manueli's Clubes — Full-Stack SaaS com pagamentos, mapas, calendário e gestão multi-tenant**

### Subtítulo curto

Nuxt · Vue · FastAPI · PostgreSQL · Redis · Celery · Stripe · Docker · CI

### Versão curta para secção de projetos

Desenvolvi um SaaS full-stack para gestão de clubes com frontend em Nuxt/Vue e backend em FastAPI, incluindo autenticação JWT, RBAC, multi-tenancy, dashboard com métricas, mapas interativos, calendário de clubes, subscrições via Stripe e processamento assíncrono de webhooks com Celery. O projeto reúne 34 endpoints REST, 72 testes automatizados, 84% de cobertura e pipeline de CI com quality gates.

### Versão final pronta a colar no CV — 3 bullets

- Desenvolvi um **SaaS full-stack** para gestão de clubes com **Nuxt/Vue no frontend** e **FastAPI no backend**, cobrindo autenticação **JWT**, **RBAC**, multi-tenancy por organização, planos e notificações.
- Implementei funcionalidades end-to-end como **dashboard com métricas**, **mapas interativos com Leaflet**, **calendário de clubes**, gestão de memberships e **pagamentos recorrentes com Stripe** apoiados por webhooks assíncronos com **Celery**.
- Estruturei o projeto com **34 endpoints REST, 72 testes automatizados, 84% de cobertura, Redis para cache/rate limiting, Docker Compose com 5 serviços** e **CI** com testes, lint e build Docker da API.

### Versão mais forte para vagas full-stack

- Concebi e implementei de ponta a ponta uma plataforma SaaS para gestão de clubes, combinando frontend em **Nuxt/Vue** com backend em **FastAPI**, autenticação segura e regras de negócio por perfil e organização.
- Entreguei fluxos completos de produto com **dashboard analítico, mapas, calendário, subscrições pagas, emails transacionais e notificações**, integrando frontend, API, Stripe e processamento assíncrono.
- Mantive foco em qualidade e operação com **testes automatizados, CI, Docker Compose, Redis, Celery, documentação técnica e controlo de abuso via rate limiting**.

### Stack a colocar no CV

**Nuxt, Vue 3, JavaScript, FastAPI, Python, SQLAlchemy, PostgreSQL, Redis, Celery, Stripe, JWT, Docker Compose, GitHub Actions, Chart.js, Leaflet, FullCalendar**

### Quando esta versão é melhor

- vagas full-stack
- startups e product teams
- vagas onde ownership end-to-end pesa muito
- vagas com componente forte de produto, UX funcional e integrações reais

---

## Headlines Para O Topo Do CV

### Se quiseres vender backend

- **Backend Developer | Python, FastAPI, APIs, Stripe, Celery, Redis**
- **Python Backend Developer | SaaS, Payments, Webhooks, Multi-Tenancy**
- **Backend Engineer | FastAPI, PostgreSQL, Redis, Async Processing**

### Se quiseres vender full-stack

- **Full-Stack Developer | Nuxt, Vue, FastAPI, PostgreSQL, Redis**
- **Full-Stack Engineer | SaaS, Payments, Dashboards, APIs**
- **Full-Stack Developer | Product-minded, API-first, end-to-end delivery**

---

## O Que Eu Escolheria Em Cada Tipo De CV

### CV Backend

Usaria esta estrutura:

- headline orientada a backend
- projeto com versão **Backend**
- menos destaque visual para Chart.js/Leaflet/Bootstrap
- mais destaque para Stripe, Celery, Redis, JWT, testes e CI

### CV Full-Stack

Usaria esta estrutura:

- headline orientada a full-stack
- projeto com versão **Full-Stack**
- manter dashboards, mapas, calendário e pagamentos no mesmo bloco
- ainda assim preservar os números concretos: endpoints, testes, coverage, serviços Docker

---

## Versão Ultra Curta Para LinkedIn / Campo De Projeto

### Backend

Backend de um SaaS para gestão de clubes com FastAPI, PostgreSQL, Redis, Celery e Stripe. Inclui JWT, RBAC, multi-tenancy, webhooks assíncronos, cache, rate limiting, 34 endpoints REST e 72 testes automatizados.

### Full-Stack

SaaS full-stack para gestão de clubes com Nuxt/Vue e FastAPI, incluindo dashboard, mapas, calendário, pagamentos com Stripe, webhooks assíncronos, RBAC, multi-tenancy e 72 testes automatizados.

---

## Recomendação Direta

Se vais candidatar-te a:

- **Backend Python**: usa a versão **Backend**
- **Full-Stack / Product Engineer**: usa a versão **Full-Stack**

A versão backend está mais forte do que a full-stack em termos de maturidade técnica percebida. Se o teu objetivo imediato é maximizar taxa de resposta, eu usaria primeiro a versão backend para vagas Python/FastAPI.

---

## Nota Importante

Quando enviares os teus PDFs, eu faço a adaptação exata para:

- o espaço real disponível no CV
- o teu tom atual
- a senioridade que queres projetar
- a coerência com o resto da experiência profissional
