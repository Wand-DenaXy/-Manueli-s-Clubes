<div align="center">

# Rate Limiting — Manueli's Clubes

**Proteção contra abuso, brute-force e sobrecarga da API**

</div>

---

## O que é Rate Limiting?

Rate Limiting é um **mecanismo de controlo de tráfego** que limita o número de pedidos HTTP que um cliente pode fazer numa janela de tempo. Quando o limite é excedido, a API rejeita os pedidos com **HTTP 429 Too Many Requests** até a janela resetar.

Sem rate limiting, qualquer IP pode fazer milhares de pedidos por segundo — sobrecarregando a base de dados, expondo endpoints de login a ataques de dicionário, ou simplesmente tornando a API inacessível para outros utilizadores.

---

## Algoritmo usado — Fixed Window Counter

O SlowAPI usa por defeito o algoritmo **Fixed Window**:

```
Janela de 1 minuto fixa no tempo:

  00:00 ──────────────────────────── 01:00
  |  req1 ✓  req2 ✓  req3 ✓  req4 ✓  req5 ✓  req6 ✗ (429)  |
  |                                                             |
  contadores armazenados no Redis com TTL = duração da janela
```

Cada IP tem uma chave no Redis no formato:
```
slowapi/<ip>/<metodo>/<rota>
```
Exemplo real: `slowapi/192.168.1.1/POST/auth/token` → valor `3` com TTL `47s`

---

## Implementação neste projeto

### Biblioteca: SlowAPI

[SlowAPI](https://github.com/laurents/slowapi) é o wrapper oficial do `Limits` para FastAPI. Usa o Redis já existente no projeto como storage dos contadores — sem infraestrutura adicional.

### Ficheiro criado: `api/app/limiter.py`

```python
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,       # identifica clientes pelo IP
    storage_uri=os.getenv("REDIS_URL"), # Redis partilhado com cache e Celery
    default_limits=["100/minute"],      # limite global aplicado a todos os endpoints
)
```

### Registo no `main.py`

```python
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
```

- `app.state.limiter` — torna o limiter acessível ao middleware
- `RateLimitExceeded` handler — converte a exceção interna em HTTP 429 com headers standard
- `SlowAPIMiddleware` — aplica o limite global a **todos os endpoints** automaticamente

### Limites por endpoint — `api/app/auth.py`

| Endpoint | Limite | Motivo |
|---|---|---|
| `POST /auth/token` (login) | **5/minuto** por IP | Bloqueia brute-force de passwords |
| `POST /auth/` (registo) | **10/minuto** por IP | Impede criação em massa de contas |
| Todos os outros | **100/minuto** por IP | Proteção geral contra abuso |

```python
@router.post("/token", response_model=Token)
@limiter.limit("5/minute")               # sobrepõe o limite global de 100/min
async def login(request: Request, ...):
    ...
```

---

## O que acontece quando o limite é excedido

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 47
Content-Type: application/json

{"error": "Rate limit exceeded: 5 per 1 minute"}
```

O header `Retry-After: 47` indica quantos segundos faltam até a janela resetar. Clientes bem implementados respeitam este header e fazem backoff automático.

---

## Vantagens

| Vantagem | Detalhe |
|---|---|
| **Proteção brute-force** | 5 tentativas/min no login torna um ataque de dicionário de 10.000 palavras-passe demorar 33 horas em vez de segundos |
| **Proteção DoS** | Um único IP não consegue saturar a API nem a base de dados |
| **Zero infraestrutura extra** | Usa o Redis já existente no projeto (broker do Celery + cache) |
| **Resposta padronizada** | HTTP 429 com `Retry-After` — compatível com todas as bibliotecas HTTP |
| **Escalável com múltiplos workers** | Contadores no Redis são partilhados entre todos os processos uvicorn |
| **Granularidade por endpoint** | Endpoints sensíveis têm limites mais restritos que os normais |

---

## Desvantagens e Limitações

| Limitação | Explicação | Mitigação possível |
|---|---|---|
| **IP spoofing / NAT** | Utilizadores atrás de NAT partilham o mesmo IP público — um pode bloquear os outros | Usar user_id como key para utilizadores autenticados |
| **Reverse proxy** | No Render/Nginx, o IP visto pode ser sempre o IP do proxy | Configurar `FORWARDED_ALLOW_IPS` e ler `X-Forwarded-For` |
| **Redis como SPOF** | Se o Redis cair, o limiter pode falhar | Configurar `on_breach=" ignore"` para fail-open |
| **Fixed Window boundary** | Um cliente pode fazer 100 req nos últimos segundos de uma janela + 100 nos primeiros da seguinte = 200 req em poucos segundos | Usar Sliding Window (mais preciso, mais consumo de memória) |
| **Não distingue utilizadores** | Limite por IP trata um admin e um anónimo da mesma forma | Dois limiters: um por IP (anónimos), um por user_id (autenticados) |

---

## Nota para produção (Render / Docker)

Quando a API corre atrás de um reverse proxy, o IP real do cliente vem no header `X-Forwarded-For`. É necessário configurar o middleware para confiar nesse header:

```python
# Em main.py, antes do SlowAPIMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
```

Sem isto, todos os utilizadores partilham o mesmo IP (o do proxy) e o rate limit afeta toda a gente ao mesmo tempo.
