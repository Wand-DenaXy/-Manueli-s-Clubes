# Roadmap e Texto CV — Manueli's Clubes

## Veredicto Rápido

- Qualidade do projeto como peça de portefólio: `8/10`
- Forma como o projeto se vende hoje: `6.5/10`
- Potencial de venda com posicionamento melhor: `8.5/10`
- Senioridade que o projeto sinaliza: `Júnior alto / Pleno inicial`

O backend já comunica maturidade suficiente para te distinguir da média de portefólio júnior. O que te impede de vender isto ainda melhor não é a falta de features, é a falta de foco no impacto, no posicionamento de negócio e no acabamento do frontend.

---

## O Que Este Projeto Prova

- Consegues construir um produto end-to-end, não apenas uma API isolada.
- Sabes integrar pagamentos reais, webhooks assíncronos, cache, autenticação e RBAC.
- Sabes estruturar um backend com testes automatizados e quality gates.
- Sabes documentar arquitetura e explicar decisões técnicas com clareza.
- Já resolves problemas que aparecem em produto real: idempotência, limites por plano, multi-tenancy e retries.

---

## Métricas Verificadas no Repo

Usa estas métricas no CV e em entrevistas porque estão alinhadas com o código e a documentação atual.

- `34 REST endpoints`
- `72 testes automatizados`
- `84% coverage` no artefacto de cobertura presente no repo
- `9 modelos ORM`
- `16 schemas Pydantic`
- `3 perfis RBAC`: Administrador, Gestor e Cliente
- `5 serviços` em Docker Compose: db, redis, api, worker, frontend
- `Rate limiting` com `10/min` em registo, `5/min` em login e `100/min` global
- `Stripe Checkout + webhooks assíncronos com Celery`
- `Multi-tenancy` por organização

Se voltares a correr CI e a cobertura mudar, atualiza este número antes de o usares em CV ou LinkedIn.

---

## Texto Pronto Para CV

### Versão Curta PT

Desenvolvi um SaaS full-stack para gestão de clubes com pagamentos recorrentes via Stripe, webhooks assíncronos com Celery, multi-tenancy por organização, RBAC, cache Redis e autenticação JWT. O projeto inclui 34 endpoints REST, 72 testes automatizados, 84% de cobertura e pipeline de CI com quality gates.

### Versão Curta EN

Built an end-to-end full-stack SaaS for club management with Stripe recurring payments, asynchronous webhook processing with Celery, organization-based multi-tenancy, RBAC, Redis caching, and JWT authentication. The project includes 34 REST endpoints, 72 automated tests, 84% coverage, and a CI pipeline with quality gates.

### Versão CV PT — 3 bullets

- Desenvolvi um SaaS full-stack para gestão de clubes com FastAPI, Nuxt, PostgreSQL e Redis, suportando autenticação JWT, RBAC e multi-tenancy por organização.
- Implementei pagamentos recorrentes com Stripe Checkout e processamento assíncrono de webhooks com Celery, incluindo idempotência, retries e envio automático de emails transacionais.
- Estruturei a API com 34 endpoints REST, 72 testes automatizados, 84% de cobertura e pipeline de CI com validação de testes, lint e build da imagem Docker da API.

### Versão CV EN — 3 bullets

- Built a full-stack SaaS for club management using FastAPI, Nuxt, PostgreSQL, and Redis, with JWT authentication, RBAC, and organization-based multi-tenancy.
- Implemented recurring payments with Stripe Checkout and asynchronous webhook processing with Celery, including idempotency, retries, and automated transactional emails.
- Structured the backend around 34 REST endpoints, 72 automated tests, 84% coverage, and a CI pipeline validating tests, linting, and API Docker image build.

### Versão LinkedIn / Portfolio Pitch

Manueli's Clubes é um projeto SaaS full-stack construído de raiz para gerir clubes, membros, mapas, calendário e subscrições pagas. O foco não foi apenas CRUD: o projeto inclui autenticação JWT, RBAC, multi-tenancy, pagamentos reais com Stripe, processamento assíncrono de webhooks com Celery, cache Redis com invalidação por prefixo, rate limiting e uma base de testes automatizados que valida fluxos críticos do produto.

---

## Como Vender Melhor O Projeto

Hoje o projeto é vendido sobretudo como “tem muitas tecnologias”. Isso ajuda, mas não é suficiente. A venda mais forte é esta:

- Problema: gestão de clubes e comunidades com perfis diferentes, limites por plano e pagamentos recorrentes.
- Solução: uma plataforma SaaS com controlo de acesso, subscrições, webhooks assíncronos, notificações e métricas operacionais.
- Complexidade real resolvida: idempotência em Stripe, retries, cache, multi-tenancy e rate limiting.
- Evidência: testes, CI, documentação técnica e infraestrutura Docker.

Regra prática: em CV, o stack vem depois do impacto. Primeiro dizes o que construíste e porque isso é difícil. Só depois dizes com que tecnologias o fizeste.

---

## Roadmap Recomendado

### Fase 1 — Melhorias que mais aumentam valor de portefólio

- Centralizar chamadas à API com runtime config em vez de `localhost` hardcoded no frontend.
  Meta mensurável: `100%` das chamadas HTTP a usar config por ambiente.
- Remover manipulação direta do DOM em páginas Vue e migrar para estado reativo e componentes.
  Meta mensurável: `0` usos de `document.getElementById` e `querySelector` nas páginas principais.
- Adicionar validação real do frontend na pipeline.
  Meta mensurável: job de `frontend build` verde em CI.
- Corrigir e estabilizar o frontend para que o projeto compile de forma previsível em ambiente limpo.
  Meta mensurável: build local e build CI reproduzíveis sem ajustes manuais.

### Fase 2 — Melhorias que sobem o nível técnico

- Introduzir migrações com Alembic em vez de depender de `create_all`.
  Meta mensurável: schema versionado e deploy sem criação implícita de tabelas.
- Fechar CORS por ambiente e endurecer configurações de produção.
  Meta mensurável: allowlist explícita por domínio e documentação de ambientes.
- Adicionar observabilidade mínima.
  Meta mensurável: request IDs, logs estruturados, monitorização de falhas em webhooks e alertas de erro.
- Cobrir rate limit com testes automatizados e acrescentar testes de integração mais próximos de produção.
  Meta mensurável: testes dedicados para `429` e cobertura backend `>= 90%`.

### Fase 3 — Melhorias de produto com valor real

- Fluxo de onboarding para nova organização.
  Meta mensurável: criar organização, admin inicial e plano inicial em menos de `10 minutos`.
- Gestão de membros mais completa: convites, aprovações e perfis por clube.
  Meta mensurável: reduzir passos de entrada de novo membro para `<= 3`.
- Notificações úteis de retenção: lembretes, pagamentos falhados, renovação e atividade do clube.
  Meta mensurável: taxa de recuperação de pagamentos falhados `> 20%` em pilotos.
- Dashboard com métricas de negócio para admins de organização.
  Meta mensurável: mostrar clubes ativos, membros ativos, inscrições por mês, conversão de plano e churn.

### Fase 4 — Melhorias de negócio

- Definir ICP em vez de servir “todos os clubes”.
  Sugestão: associações pequenas, clubes desportivos locais ou comunidades de hobby com gestão simples.
- Clarificar a dor principal.
  Sugestão: “gestão de membros + cobrança + calendário + comunicação” num único produto.
- Criar uma proposta de valor mensurável.
  Exemplo: reduzir gestão manual, centralizar pagamentos e evitar falhas de cobrança.
- Fazer validação com utilizadores reais.
  Meta mensurável: `10` entrevistas com potenciais utilizadores e `3` pilotos reais.

---

## Ideias de Negócio Que Fazem Mais Sentido

Se quiseres que o projeto tenha mais força comercial, o melhor passo não é adicionar mais features genéricas. É estreitar o alvo.

### Opção A — Associações e clubes locais

- Dor: gestão manual em Excel/WhatsApp, cobrança solta e pouca visibilidade.
- Valor: membros, eventos, mapas e pagamentos numa única plataforma.
- Porque faz sentido: é o teu posicionamento atual mais natural.

### Opção B — Comunidades privadas / membership clubs

- Dor: gerir comunidade, convites, pagamentos e calendário em ferramentas dispersas.
- Valor: experiência mais premium e centrada em membros pagantes.
- Porque faz sentido: encaixa bem com Stripe, planos e notificações.

### Opção C — Micro-SaaS para organizadores de grupos recorrentes

- Dor: inscrições, eventos, presenças e pagamento recorrente num fluxo simples.
- Valor: produto mais estreito, mais fácil de vender e mais fácil de validar.
- Porque faz sentido: melhor foco para MVP comercial real.

---

## Métricas de Produto Que Deves Passar a Acompanhar

Se quiseres vender o projeto com mais peso, começa a falar também em métricas de produto e operação.

- Tempo até primeiro valor: tempo entre registo e criação do primeiro clube.
- Ativação: percentagem de utilizadores que criam pelo menos 1 clube e 1 evento.
- Conversão Free → Pago.
- Taxa de falha de pagamento.
- Taxa de recuperação após pagamento falhado.
- Clubes ativos por organização.
- Inscrições por evento/clube.
- Latência média dos endpoints principais.
- Tempo de processamento de webhook.
- Cache hit ratio para `/stats`, `/clubes`, `/mapas` e `/planos`.

---

## O Que Eu Acharia Forte Ver Num CV Teu

- Um título claro: `Full-Stack SaaS Project` ou `Backend-heavy SaaS with Payments and Async Processing`.
- Impacto logo na primeira linha, antes da stack.
- Métricas concretas em pelo menos `2` bullets.
- Uma bullet só para pagamentos/webhooks assíncronos.
- Uma bullet só para testes/CI/infra.
- Menos lista de tecnologias, mais prova de decisão técnica.

---

## Erros Comuns Ao Vender Este Projeto

- Falar só de CRUD e não falar de pagamentos, webhooks, retries e multi-tenancy.
- Listar tecnologia sem explicar o problema resolvido.
- Dizer `CI/CD` quando o repo prova sobretudo `CI`.
- Dizer `93% coverage` se o estado atual do repo já não suporta esse número.
- Colocar demasiadas bullets pequenas no CV em vez de `2` ou `3` bullets fortes com números.

---

## Avaliação de “Venda” de 0 a 10

### Projeto em si

- `8/10`

Porque resolve problemas reais, cobre backend, frontend, infraestrutura e integrações externas, e já tem documentação técnica acima da média.

### Como o projeto está atualmente posicionado

- `6.5/10`

Porque ainda está ligeiramente mais centrado em stack do que em impacto, e algumas partes do frontend reduzem a perceção de acabamento global.

### Potencial se o venderes bem no CV e entrevista

- `8.5/10`

Porque com o framing certo passas de “projeto académico grande” para “produto full-stack com integrações e problemas reais de engenharia”.

---

## Revisão do CV — Estado Atual

Os teus CVs **não vieram nos anexos desta conversa** e não existem ficheiros de CV no workspace atual. Por isso ainda não consigo dizer se estás a vender bem o teu perfil no documento em si.

Assim que enviares o CV, eu consigo analisar:

- headline profissional
- clareza do resumo
- qualidade das métricas
- força dos verbos de ação
- densidade técnica correta
- coerência entre o que o CV promete e o que o projeto prova
- nota final de venda pessoal de `0 a 10`

---

## Como Me Enviar O CV Na Próxima Mensagem

- Anexa o PDF ou DOCX.
- Ou cola o conteúdo do CV na conversa.
- Ou indica o ficheiro se estiver noutro workspace.

Quando enviares, eu faço revisão linha a linha e digo exatamente:

- o que está forte
- o que está fraco
- o que está genérico
- o que está a vender abaixo do teu valor
- versão melhorada pronta a usar
