# 03 — Landscape dos projetos-alvo

Pesquisa read-only dos três projetos fornecidos no repositório base. Serve de **insumo** para o catálogo da skill e para a Análise Manual futura no README (não substitui a seção “Análise Manual” do entregável).

## Visão comparativa

| Aspecto | `code-smells-project` | `ecommerce-api-legacy` | `task-manager-api` |
|---------|----------------------|------------------------|--------------------|
| Linguagem | Python | Node.js (CommonJS) | Python |
| Framework | Flask 3.1.1 | Express ^4.18.2 | Flask 3.0.0 |
| Persistência | SQLite arquivo (`loja.db`) | sqlite3 **:memory:** | SQLite + SQLAlchemy (`tasks.db`) |
| Organização | Flat pseudo-MVC (4 módulos) | God class `AppManager` | Camadas parciais (models/routes/services) |
| Porta default | 5000 | 3000 | 5000 |
| Entrypoint | `python app.py` | `npm start` → `node src/app.js` | `python seed.py` + `python app.py` |
| Domínio | E-commerce (produtos, pedidos, usuários) | LMS + checkout | Task Manager |

**Implicação:** a skill deve lidar com monólito extremo **e** projeto já “quase MVC”, além de duas stacks.

---

## Projeto 1 — `code-smells-project/`

### Estrutura atual

```
code-smells-project/
├── app.py           # wiring + endpoints admin perigosos
├── controllers.py   # handlers HTTP
├── models.py        # SQL + “lógica” (não é ORM)
├── database.py      # conexão singleton + schema/seed
├── requirements.txt # flask, flask-cors
└── README.md
```

### Stack / domínio

- API REST de loja: produtos, usuários, login, pedidos, relatório de vendas, health
- Rotas em português (`/produtos`, `/pedidos`, …)
- Sem ORM — `sqlite3` raw

### Smells evidenciados (candidatos para catálogo)

| Severidade | Smell | Evidência |
|------------|-------|-----------|
| CRITICAL | Execução de SQL arbitrário | `app.py` — `POST` admin com `cursor.execute(query)` do body |
| CRITICAL | SQL Injection | `models.py` — login/busca com concatenação de strings |
| CRITICAL | Senhas em plaintext + vazamento | `models.py` / listagem de usuários retorna `senha` |
| HIGH | Admin reset sem auth + health vaza secret | `app.py`, health em controllers |
| HIGH | N+1 em pedidos | loops com cursors aninhados em `models.py` |
| MEDIUM | Validação duplicada / side effects via `print` | `controllers.py` |
| MEDIUM | Singleton DB `check_same_thread=False` | `database.py` |
| LOW | `SECRET_KEY` hardcoded, `debug=True` | `app.py` |

### Validação pós-refatoração (smoke)

1. `pip install -r requirements.txt && python app.py`
2. `GET /health`, `GET /`, `GET /produtos`
3. `POST /login` com usuário seed; fluxo de pedido
4. Garantir que admin SQL / reset perigosos foram removidos ou protegidos

---

## Projeto 2 — `ecommerce-api-legacy/`

### Estrutura atual

```
ecommerce-api-legacy/
├── package.json
├── api.http
└── src/
    ├── app.js         # bootstrap fino
    ├── AppManager.js  # schema + seed + todas as rotas
    └── utils.js       # config, cache, “crypto”
```

### Stack / domínio

- LMS: users, courses, enrollments, payments, audit
- Checkout com cartão fake; relatório financeiro admin; delete user
- DB em memória — **restart zera estado** (validação na mesma sessão do processo)

### Smells evidenciados

| Severidade | Smell | Evidência |
|------------|-------|-----------|
| CRITICAL | Log de cartão + chave de gateway | `AppManager.js` checkout + `utils.js` |
| CRITICAL | Credenciais hardcoded | `utils.js` (`dbPass`, `paymentGatewayKey`, SMTP) |
| HIGH | Hash fraco `badCrypto` + senha seed `123` | `utils.js`, seed |
| HIGH | Checkout em callback hell (registro+pagamento+audit) | `AppManager.js` |
| HIGH | Race no financial report (`forEach` + contadores async) | `AppManager.js` |
| MEDIUM | DELETE user sem limpar FKs | `AppManager.js` |
| MEDIUM | Body criptico sem validação (`usr`, `eml`, `cc`) | checkout |
| LOW | `globalCache` / dead state | `utils.js` |

### Deprecated / legado

- API callback-only do `sqlite3` (preferível promisify / better-sqlite3 no playbook moderno)
- Sem routers Express, sem middlewares de erro/auth

### Validação pós-refatoração

1. `npm install && npm start` — porta 3000
2. Usar `api.http`: checkout card `4…` OK / `5…` deny; financial-report; delete user
3. Totais do report devem ser consistentes após correção de race

---

## Projeto 3 — `task-manager-api/`

### Estrutura atual

```
task-manager-api/
├── app.py
├── database.py
├── seed.py
├── models/       # user, task, category (SQLAlchemy)
├── routes/       # task, user, report (+ categories no report_bp)
├── services/     # notification_service (não usado)
├── utils/helpers.py
└── requirements.txt  # inclui marshmallow/requests/dotenv não usados
```

### Stack / domínio

- Tasks, users/roles, categories, login fake-token, reports/summary, search/stats
- Melhor organização dos três — **ainda não é MVC adequado**

### Smells evidenciados

| Severidade | Smell | Evidência |
|------------|-------|-----------|
| CRITICAL | `to_dict()` expõe password hash; token fake sem enforcement | `models/user.py`, `user_routes.py` |
| HIGH | MD5 para senha; SMTP password hardcoded no service | `user.py`, `notification_service.py` |
| HIGH | Lógica overdue / serialização duplicada nas routes | `task_routes.py` vs `Task.is_overdue` |
| HIGH | N+1 em listagens e reports em memória | `task_routes.py`, `report_routes.py` |
| MEDIUM | Service morto (nunca importado) | `services/notification_service.py` |
| MEDIUM | CRUD de categories no `report_bp` | bounded context errado |
| MEDIUM | `except:` genérico engolindo erros | várias routes |
| LOW | Deps não usadas; config legada | `requirements.txt`, `SQLALCHEMY_TRACK_MODIFICATIONS` |

### APIs deprecated (obrigatório no catálogo)

| Sinal | Moderno |
|-------|---------|
| `datetime.utcnow()` | `datetime.now(timezone.utc)` |
| `Model.query.get(id)` | `db.session.get(Model, id)` (SQLAlchemy 2.0) |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | Remover / ignorar em Flask-SQLAlchemy 3.x |

### Validação pós-refatoração

1. `pip install -r requirements.txt && python seed.py && python app.py`
2. `GET /health`, `/`, `/tasks`, `/tasks/stats`, `/reports/summary`
3. CRUD tasks/users/categories; login seed
4. Rodar **um Flask por vez** na porta 5000 (conflito com projeto 1)

### Adaptação da Fase 3

Não destruir blueprints/ORM à toa. Preferir:

- Extrair controllers a partir de fat routes
- Config/env sem secrets
- Error handler central
- Remover dead code / realinhar categories
- Corrigir segurança e N+1 mantendo contratos de endpoint

---

## Implicações transversais para a skill

1. **Detecção de stack:** `requirements.txt` + imports Flask vs `package.json` + Express
2. **Arquitetura atual:** flat / god-class / partial-layers — condiciona profundidade do rebuild
3. **Deprecated:** pelo menos um finding de API obsoleta no projeto 3 (e recomendações no Node para callbacks)
4. **Validação:** descobrir porta, entrypoint e endpoints na Fase 1; usar `api.http` quando existir
5. **Catálogo mínimo** deve cobrir smells que aparecem em ≥1 projeto e generalizar sinais

Próximo: decisões de design → [`04-skill-design-implications.md`](./04-skill-design-implications.md)
