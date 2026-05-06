<div align="center">

# Teoria do Projeto — Manueli's Clubes

**Análise técnica completa da arquitetura, padrões e decisões de design**

</div>

---

## 1. Visão Geral da Arquitetura

```
┌─────────────────┐     HTTP/JSON      ┌──────────────────────┐
│  Nuxt 3 / Vue 3 │ ─────────────────► │  FastAPI (uvicorn)   │
│  (port 3000)    │ ◄───────────────── │  (port 8000)         │
└─────────────────┘                    └──────────┬───────────┘
                                                   │
                              ┌────────────────────┼────────────────────┐
                              ▼                    ▼                    ▼
                    ┌──────────────┐    ┌──────────────────┐   ┌──────────────┐
                    │  PostgreSQL  │    │      Redis       │   │  Stripe API  │
                    │  (port 5432) │    │  (port 6379)     │   │  (external)  │
                    └──────────────┘    └────────┬─────────┘   └──────────────┘
                                                  │
                                        ┌─────────▼─────────┐
                                        │  Celery Worker    │
                                        │  (async tasks)    │
                                        └───────────────────┘
```

O projeto é um **SaaS full-stack de 5 serviços** orquestrados por Docker Compose. Cada serviço tem responsabilidade única (princípio da separação de responsabilidades).

---

## 2. Backend — FastAPI

### Por que FastAPI?

FastAPI é um framework Python assíncrono baseado em **ASGI** (Asynchronous Server Gateway Interface). Vantagens sobre Flask/Django neste contexto:

- **Validação automática** via Pydantic — inputs inválidos retornam HTTP 422 sem código extra
- **Documentação automática** — Swagger UI em `/docs` gerada a partir das anotações de tipo
- **Async nativo** — pedidos I/O-bound (BD, Redis, Stripe) não bloqueiam o event loop
- **Dependency Injection** — `Depends()` para sessões de BD, autenticação e roles

### Estrutura dos endpoints

Todos os endpoints seguem o padrão:
```
Receber request → Validar (Pydantic) → Verificar auth (JWT) → Verificar role (RBAC)
→ Verificar cache (Redis) → Executar lógica de negócio → Invalidar cache → Retornar response
```

---

## 3. Autenticação — JWT + Argon2id

### Fluxo
```
POST /auth/token
  → recebe username + password
  → carrega user da BD
  → bcrypt_context.verify(password, user.password_hash)  ← Argon2id
  → jwt.encode({sub, id, tipo_id, org_id, exp}, SECRET_KEY, HS256)
  → retorna {access_token, token_type: "bearer"}

Endpoints protegidos:
  → Authorization: Bearer <token>
  → get_current_user() → jwt.decode() → carrega user da BD
  → injeta user como dependência na função de rota
```

### Por que Argon2id?

Argon2id é o vencedor da **Password Hashing Competition (2015)** e a recomendação atual do OWASP. É resistente a ataques GPU/ASIC porque usa intensidade de memória configurável — ao contrário de bcrypt que é apenas CPU-bound.

### Por que JWT e não sessions?

JWT é **stateless** — o servidor não precisa guardar estado de sessão. Escala horizontalmente sem sessão partilhada. O token expira em 30 minutos, limitando a janela de exposição em caso de roubo.

---

## 4. RBAC — Role-Based Access Control

```
Administrador  →  acesso total (CRUD tudo, todas as organizações)
Gestor         →  criar/editar clubes e mapas da sua organização
Cliente        →  ler dados, ingressar em clubes, gerir plano
```

### Implementação

```python
def require_roles(*roles: str):
    def role_checker(user = Depends(get_current_user)):
        if user.tipo.descricao not in roles:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return role_checker

# Uso:
@app.delete("/clubes/{id}")
def delete_clube(user = Depends(require_roles("Administrador"))):
    ...
```

A função `require_roles` retorna uma **closure** que é usada como dependência FastAPI — elegante e sem repetição de código.

---

## 5. Multi-tenancy por Organização

Cada utilizador pertence a uma `Organization`. Todos os dados de negócio (clubes, mapas) têm `organization_id` como foreign key.

```
OrganizationModel (1)
    └── UtilizadorModel (N)  →  só vê clubes da sua organização
    └── ClubeModel (N)       →  filtrado por organization_id em cada query
            └── MapaModel (N)
            └── MembroClubeModel (N)
```

O endpoint `GET /clubes` filtra sempre por `user.organization_id` — um utilizador nunca vê dados de outra organização sem código extra de verificação.

---

## 6. Cache — Redis com TTL e Invalidação por Prefixo

### Problema que resolve

Queries como `SELECT COUNT(*) FROM clubes` ou listas completas de utilizadores são executadas em cada pedido. Com caching, a query é feita uma vez e o resultado guardado no Redis com um TTL.

### Pattern Cache-Aside

```
receber pedido GET
  → cache_get("clubes:org:5:list")
    → HIT:  retornar imediatamente (0 queries à BD)
    → MISS: executar query SQL → cache_set(resultado, ttl=30) → retornar

receber pedido POST/PUT/DELETE
  → executar operação na BD
  → cache_invalidate("clubes:")  ← elimina todas as chaves com este prefixo
```

### Invalidação por prefixo

```python
def cache_invalidate(*prefixes: str):
    for prefix in prefixes:
        for key in _redis.scan_iter(f"{prefix}*"):
            _redis.delete(key)
```

Usar `SCAN` em vez de `KEYS` é importante em produção — `KEYS` bloqueia o Redis enquanto itera, `SCAN` é incremental e não-bloqueante.

| Cache Key | TTL | Invalidado por |
|---|---|---|
| `stats` | 60s | CRUD clubes/utilizadores |
| `clubes:org:{id}:list` | 30s | POST/PUT/DELETE /clubes |
| `utilizadores:list` | 30s | PUT/DELETE /utilizadores |
| `tipouser:list` | 120s | CRUD /tipouser |
| `mapas:list` | 60s | POST/PUT/DELETE /mapas |
| `planos:list` | 120s | CRUD /planos |
| `registrations:{year}` | 300s | — (dados históricos) |

---

## 7. Pagamentos — Stripe Checkout + Webhooks

### Fluxo completo

```
1. User clica "Subscrever Pro"
2. POST /create-checkout-session → cria Stripe Session (server-side)
3. API retorna {url} → frontend redireciona para Stripe
4. User insere cartão no Stripe (PCI compliant — nunca passa pelo servidor)
5. Stripe processa pagamento
6. Stripe envia POST /stripe/webhook com evento assinado (HMAC-SHA256)
7. API verifica assinatura → enfileira Celery task
8. Celery worker:
   a. Verifica idempotência (event_id já processado?)
   b. Atualiza plano do utilizador na BD
   c. Cria notificação
   d. Envia email HTML
   e. Guarda event_id na BD
9. Stripe recebe HTTP 200 → considera entregue
```

### Por que processar o webhook em Celery e não diretamente?

O Stripe tem um **timeout de 30 segundos** para o webhook. Se a lógica de negócio (query BD + email SMTP) demorar mais, o Stripe considera falha e reencaminha o evento. Com Celery:
- O endpoint responde em <100ms (`{"status": "queued"}`)
- O worker processa no seu próprio tempo
- Retry automático em caso de falha

---

## 8. Celery — Processamento Assíncrono, Retry & Backoff

```
FastAPI worker  ──enfileira──►  Redis (broker)  ──consome──►  Celery worker
    (HTTP)                      (queue)                        (task)
```

### Retry & Backoff

Falhas temporárias (BD sobrecarregada, SMTP indisponível, timeout Stripe) não devem ser erros permanentes. O Celery tenta novamente automaticamente com **exponential backoff**:

```python
@celery.task(
    bind=True,
    max_retries=5,
    default_retry_delay=30,
    autoretry_for=(Exception,),
    retry_backoff=True,        # 30s → 60s → 120s → 240s → 480s
    retry_backoff_max=600,     # máximo 10 minutos entre retries
)
```

| Tentativa | Espera | Razão |
|---|---|---|
| 1ª retry | 30 s | falha transitória comum |
| 2ª retry | 60 s | dar tempo ao serviço para recuperar |
| 3ª retry | 120 s | backoff progressivo |
| 4ª retry | 240 s | serviço ainda em recuperação |
| 5ª retry | 480 s | última tentativa antes de DLQ |

**Por que backoff exponencial e não intervalo fixo?**  
Com intervalo fixo, todos os workers em retry batem no mesmo serviço ao mesmo tempo — **thundering herd problem**. O backoff exponencial espalha os retries no tempo, reduzindo a pressão sobre o serviço que está a recuperar. O `retry_backoff_max=600` garante que nunca se espera mais de 10 minutos, evitando delays excessivos.

---

## 9. Idempotência e Deduplicação — Evitar Processar o Mesmo Evento Duas Vezes

O Stripe pode reenviar o mesmo webhook várias vezes (network failure, timeout). Sem proteção, o utilizador seria cobrado duas vezes ou mudaria de plano múltiplas vezes.

### Idempotência

Uma operação é **idempotente** quando executá-la N vezes produz exactamente o mesmo resultado que executá-la uma só vez. O sistema garante esta propriedade guardando o `event_id` do Stripe na tabela `stripe_events` — qualquer reentrada com o mesmo ID é rejeitada antes de tocar em qualquer estado.

### Deduplicação — Double-check pattern

**Deduplicação** é o mecanismo concreto que implementa a idempotência: eliminar duplicados antes de processar. São usadas duas linhas de defesa:

```
┌─────────────────────────────────────────────────────────────────┐
│  Linha 1 — Endpoint HTTP                                        │
│  POST /stripe/webhook                                           │
│    → verificar stripe_events (event_id já existe?)              │
│    → SIM: return 200 {"status": "duplicate"}  (drop silencioso) │
│    → NÃO: enfileirar Celery task                                │
└─────────────────────────────────────────────────────────────────┘
           ↓  (múltiplos workers podem receber o mesmo evento)
┌─────────────────────────────────────────────────────────────────┐
│  Linha 2 — Celery Worker                                        │
│    → verificar novamente dentro da transação (race condition)   │
│    → processar lógica de negócio                                │
│    → INSERT stripe_events(event_id) + UPDATE utilizador.plano   │
│       numa única transação atómica                              │
└─────────────────────────────────────────────────────────────────┘
```

A verificação dupla (no endpoint **e** na task) protege contra race conditions quando múltiplos HTTP workers recebem o mesmo evento simultaneamente. A verificação na task acontece dentro da mesma transação de base de dados que guarda o `event_id`, tornando-a atómica — ver Secção 17.

---

## 17. Operações Atómicas — Consistência sob Concorrência

Uma **operação atómica** é indivisível: ou executa completamente ou não executa de todo. No sistema existem três contextos críticos onde a atomicidade é garantida:

### 17.1 Processamento de Webhook Stripe

A verificação de duplicado e o registo do evento acontecem na **mesma transação de BD**:

```python
# Dentro da Celery task — tudo ou nada
try:
    existing = db.query(StripeEventModel).filter_by(event_id=event_id).first()
    if existing:
        return {"status": "duplicate"}

    # lógica de negócio
    user.plano_id = novo_plano.id
    db.add(StripeEventModel(event_id=event_id))  # regista o evento
    db.commit()                                   # commit atómico dos dois
except Exception:
    db.rollback()                                 # nenhuma das alterações fica
    raise
```

Se o commit falhar a meio (ex: crash do processo), o rollback garante que nem o plano é alterado nem o event_id é guardado — o webhook será reprocessado na próxima tentativa sem inconsistência.

### 17.2 UniqueConstraint — Atomicidade a nível de BD

A constraint de BD na tabela `membro_clube` é uma operação atómica garantida pelo motor de base de dados:

```sql
CREATE UNIQUE INDEX uq_membro_clube
    ON membro_clube (utilizador_id, clube_id);
```

Mesmo que dois pedidos HTTP cheguem em simultâneo tentando inscrever o mesmo utilizador no mesmo clube, a BD garante atomicamente que só um `INSERT` tem sucesso — o outro recebe um erro de constraint, sem necessidade de locks explícitos na aplicação.

### 17.3 Cache Invalidation — Read-Modify-Write

As operações de escrita seguem sempre a sequência:

```
1. db.commit()           ← persistir na BD primeiro
2. cache_invalidate()    ← só depois invalidar o cache
```

Inverter a ordem criaria uma janela de inconsistência: se o processo crashasse após invalidar o cache mas antes de fazer commit, o cache ficaria vazio mas a BD teria o estado antigo. Com a ordem correcta, no pior caso o cache serve dados ligeiramente obsoletos até ao próximo TTL.

---

## 10. Sistema de Planos e Limites

```
Free:       €0/mês  →  3 clubes,   1 mapa
Pro:        €9.99   →  15 clubes, 20 mapas
Enterprise: €29.99  →  ∞ clubes,  ∞ mapas  (limite = -1)
```

### Verificação de limites

```python
if user.plano:
    limite = user.plano.limite_clubes
    if limite != -1:                               # -1 = ilimitado
        total = db.query(ClubeModel).filter(
            ClubeModel.organization_id == user.organization_id
        ).count()
        if total >= limite:
            raise HTTPException(403, f"Limite de {limite} clube(s) atingido")
```

Limite verificado **server-side** em cada criação — não pode ser contornado pelo frontend.

---

## 11. Validação e Sanitização — Pydantic

Todos os inputs passam por schemas Pydantic antes de tocar na lógica de negócio:

```python
class ClubeCreate(BaseModel):
    nome: str
    email: str
    telefone: str
    localidade: str
    evento_at: date | None = None
```

- **Tipos errados** (ex: `nome: 123`) → HTTP 422 automático
- **Campos em falta** → HTTP 422 automático
- **SQL Injection** → impossível — SQLAlchemy usa queries parametrizadas, nunca concatena strings
- **Campos extra** → ignorados por defeito (não vazam para a BD)

---

## 12. Rate Limiting — SlowAPI + Redis

Ver [ratelimit.md](ratelimit.md) para documentação completa.

**Resumo:**
- `POST /auth/token` → **5/minuto** por IP (anti brute-force)
- `POST /auth/` → **10/minuto** por IP (anti criação em massa)
- Todos os outros → **100/minuto** por IP (proteção geral)
- Contadores armazenados no Redis (partilhado entre workers)
- Resposta: HTTP 429 com header `Retry-After`

---

## 13. Frontend — Nuxt 3

```
nuxt-app/
├── pages/
│   ├── index.vue        → landing page
│   ├── login.vue        → formulário + POST /auth/token → guarda JWT em cookie
│   ├── dashboard.vue    → KPIs (stats, registrations, tipouser) + Chart.js
│   ├── clubes.vue       → CRUD clubes + ingressar
│   ├── mapas.vue        → Leaflet.js com marcadores GPS
│   ├── planos.vue       → cards de planos + Stripe Checkout
│   └── calendario.vue   → FullCalendar com eventos dos clubes
└── components/
    ├── Header.vue
    └── Navbar.vue
```

O JWT é guardado num **cookie HttpOnly** (ou localStorage dependendo da configuração) e enviado em cada pedido como `Authorization: Bearer <token>`.

---

## 14. Base de Dados — PostgreSQL + SQLAlchemy ORM

```
organizations ──< utilizador >── tipouser
      │               │
      └──< clubes     └──< membro_clube >── clubes
               │
               └──< mapas

planos ──< utilizador
stripe_events (log de idempotência)
notificacoes ──< utilizador
```

### Decisões de design

- **`autocommit=False`** — transações explícitas, rollback em caso de erro
- **`UniqueConstraint`** na tabela `membro_clube` — constraint de BD garante que um utilizador não pode ingressar no mesmo clube duas vezes, mesmo com race condition
- **`cascade="all, delete-orphan"`** — apagar um clube apaga automaticamente os seus mapas e membros
- **`index=True`** em `username` e `event_id` — queries de lookup frequentes

---

## 15. CI/CD — GitHub Actions

```yaml
Push/PR para main:
  Job 1: pytest --cov (gate: cobertura ≥ 75%)
  Job 2: ruff check (lint)
  Job 3: docker build (só corre se Job 1 e 2 passarem)
```

O gate de cobertura impede que código novo reduza drasticamente a qualidade dos testes. A build Docker valida que a imagem de produção compila sem erros.

---

## 16. Docker Compose — 5 Serviços

| Serviço | Imagem | Porta | Função |
|---|---|---|---|
| `db` | postgres:15 | 5432 | Base de dados principal |
| `redis` | redis:7-alpine | 6379 | Cache + broker Celery |
| `api` | ./api/Dockerfile | 8000 | FastAPI + uvicorn |
| `worker` | ./api/Dockerfile | — | Celery worker (mesmo código, comando diferente) |
| `frontend` | ./nuxt-app/Dockerfile | 3000 | Nuxt 3 SSR |

O `worker` usa a mesma imagem do `api` mas executa `celery -A app.celery_app worker` em vez de `uvicorn` — reutilização de imagem sem duplicar o Dockerfile.

---

## 18. Padrões de Resiliência — Sumário

O sistema aplica seis padrões de resiliência de forma coordenada. A tabela seguinte mostra onde cada padrão é aplicado e qual problema resolve:

| Padrão | Onde é aplicado | Problema que resolve |
|---|---|---|
| **Idempotência** | Webhooks Stripe (`stripe_events`) | Reprocessamento de eventos duplicados enviados pelo Stripe |
| **Deduplicação** | Double-check no endpoint + na Celery task | Race condition entre múltiplos HTTP workers |
| **Caching** | Redis (Cache-Aside, TTL + invalidação por prefixo) | Latência e carga excessiva em queries repetidas à BD |
| **Rate Limiting** | SlowAPI + Redis por IP | Brute-force, credential stuffing, abuso de API |
| **Atomic Operations** | Transações SQLAlchemy, UniqueConstraint, ordem commit→invalidate | Inconsistência de dados sob concorrência e falhas parciais |
| **Retry & Backoff** | Celery (exponential backoff, max 5 retries) | Falhas transitórias em serviços externos (BD, SMTP, Stripe) |

### Como os padrões se complementam

```
Pedido entra
  │
  ├─► Rate Limit (SlowAPI)         ← bloqueia abuso antes de chegar à lógica
  │
  ├─► Cache HIT?  ──SIM──►  responde imediatamente (sem BD)
  │       │
  │      NÃO
  │       │
  ├─► Lógica de negócio (BD)
  │       │
  │   (webhook Stripe)
  │       │
  │       ├─► Deduplicação (linha 1) — endpoint descarta duplicados
  │       │
  │       └─► Enfileira Celery task
  │               │
  │               ├─► Deduplicação (linha 2) — task verifica novamente
  │               │
  │               ├─► Operação Atómica — commit BD + registo event_id
  │               │
  │               └─► Retry & Backoff — se falhar, tenta até 5× com espera crescente
  │
  └─► Cache Invalidation — dados actualizados, cache limpo atomicamente
```

Nenhum padrão é suficiente sozinho: o Rate Limit não protege contra eventos duplicados; a Deduplicação não resolve falhas de SMTP; o Retry sem Backoff agrava falhas em cascata. A robustez do sistema vem da **combinação** destes padrões em camadas.
