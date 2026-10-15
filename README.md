# Criação de Skills — Refatoração Arquitetural Automatizada

Fork do desafio [devfullcycle/mba-ia-refactor-projects-skill](https://github.com/devfullcycle/mba-ia-refactor-projects-skill) com a skill **`refactor-arch`** (Claude Code), relatórios de auditoria e os 3 projetos refatorados para MVC.

Documentação RPI: [`docs/`](./docs/).

## A) Análise Manual

### Projeto 1 — `code-smells-project` (Python/Flask — E-commerce)

| Severidade | Problema | Por que importa |
|------------|----------|-----------------|
| CRITICAL | SQL arbitrário em `POST /admin/query` (`app.py`) | Compromete o banco inteiro |
| CRITICAL | Credenciais/SECRET_KEY hardcoded (`app.py`) | Vazamento de segredo de sessão |
| CRITICAL | Senhas plaintext + retorno na API (`models.py`) | Exposição direta de credenciais |
| HIGH | SQL injection em login/busca (`models.py`) | Bypass de auth e leitura indevida |
| HIGH | N+1 na listagem de pedidos (`models.py`) | Performance inviável com escala |
| MEDIUM | Validação/side effects no controller (`controllers.py`) | Acoplamento HTTP ↔ domínio |
| MEDIUM | Singleton DB global (`database.py`) | Estado mutável compartilhado |
| LOW | Health vazando `secret_key` (`controllers.py`) | Information disclosure |
| LOW | `debug=True` fixo no entrypoint | Risco em deploy |

### Projeto 2 — `ecommerce-api-legacy` (Node/Express — LMS checkout)

| Severidade | Problema | Por que importa |
|------------|----------|-----------------|
| CRITICAL | God class `AppManager.js` | Schema + rotas + negócio no mesmo módulo |
| CRITICAL | Secrets hardcoded (`utils.js`) | Credenciais de pagamento/SMTP no repo |
| HIGH | Log de cartão + gateway key | Vazamento de dados sensíveis de pagamento |
| HIGH | Checkout em callback hell | Fluxo frágil e não testável |
| HIGH | `badCrypto` + senha seed fraca | Autenticação trivial |
| MEDIUM | Race no financial report | Totais financeiros incorretos |
| MEDIUM | DELETE user deixa orphans | Integridade quebrada |
| LOW | Campos crípticos `usr`/`eml`/`cc` | DX e validação pobres |
| LOW | sqlite3 só com callbacks aninhados | Padrão legado |

### Projeto 3 — `task-manager-api` (Python/Flask — Task Manager)

| Severidade | Problema | Por que importa |
|------------|----------|-----------------|
| CRITICAL | `User.to_dict()` expõe password hash | Vazamento de hashes |
| HIGH | MD5 + fake JWT sem enforcement | Auth ilusória |
| HIGH | Fat routes (validação + N+1) | Camadas parciais sem MVC real |
| HIGH | N+1 em `GET /tasks` | Queries por item na listagem |
| MEDIUM | `datetime.utcnow` / `query.get` deprecated | Quebra futura |
| MEDIUM | Categories no blueprint de reports + service morto | Bounded context errado / dead code |
| MEDIUM | `except:` genérico | Erros engolidos |
| LOW | SECRET_KEY hardcoded | Config insegura |
| LOW | Deps não usadas (marshmallow, requests) | Ruído de dependências |

---

## B) Construção da Skill

### Design

- Ferramenta: **Claude Code**
- Path: `{projeto}/.claude/skills/refactor-arch/`
- Invocação: `claude "/refactor-arch"`
- `disable-model-invocation: true` (só sob comando explícito)
- Progressive disclosure: `SKILL.md` enxuto + 5 refs Markdown

```
.claude/skills/refactor-arch/
├── SKILL.md                 # 3 fases + gate [y/n]
├── project-analysis.md      # heurísticas de stack
├── anti-patterns.md         # 10 anti-patterns (CRITICAL→LOW) + deprecated APIs
├── report-template.md       # template Fase 2
├── mvc-architecture.md      # guidelines MVC + adaptação
└── refactor-playbook.md     # 10 transformações before/after
```

### Catálogo (por quê)

Cobre segurança (SQL injection, secrets, data exposure), MVC/SOLID (god class, fat controller, global state), performance (N+1), qualidade (dead code, naming) e **APIs deprecated** (`utcnow`, `query.get`, callbacks sqlite).

### Agnosticismo

Heurísticas por manifests (`requirements.txt` / `package.json`) e sinais de import — sem paths hardcoded de um único projeto. Playbook com exemplos Python e Node. Fase 3 adapta: **rebuild** (monólito) vs **realinhamento** (partial layers).

### Desafios

- Projeto 3 já tinha pastas: a skill precisa melhorar sem destruir ORM/blueprints.
- Portas Flask 5000 em conflito entre projetos 1 e 3 — validar um por vez.
- Endpoints inseguros CRITICAL: mantidos no path com 403/token em vez de sumir sem documento.

Processo RPI documentado em [`docs/`](./docs/).

---

## C) Resultados

### Findings por projeto (Fase 2)

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| 1 code-smells-project | 4 | 3 | 2 | 2 | 11 |
| 2 ecommerce-api-legacy | 2 | 3 | 2 | 2 | 9 |
| 3 task-manager-api | 1 | 3 | 3 | 2 | 9 |

Relatórios: [`reports/audit-project-1.md`](./reports/audit-project-1.md), [`audit-project-2.md`](./reports/audit-project-2.md), [`audit-project-3.md`](./reports/audit-project-3.md).

### Estrutura antes → depois

**Projeto 1**

```
antes: app.py, controllers.py, models.py, database.py
depois:
  app.py (composition root)
  src/config | models | controllers | views | middlewares
```

**Projeto 2**

```
antes: src/app.js, AppManager.js, utils.js
depois:
  src/config | models | controllers | views | middlewares | app.js
```

**Projeto 3**

```
antes: app.py + models/ + routes/ (gordas) + services morto
depois:
  config/ + controllers/ + routes finas + middlewares/
  categories fora de reports; notification_service removido
```

### Checklist de validação (3/3)

| Critério | P1 | P2 | P3 |
|----------|----|----|----|
| Fase 1 stack correta | OK | OK | OK |
| Fase 2 ≥5 findings | OK | OK | OK |
| ≥1 CRITICAL/HIGH | OK | OK | OK |
| Gate confirmação | OK | OK | OK |
| Fase 3 boot + endpoints | OK | OK | OK |

### Logs de validação (pós-refatoração)

- **P1:** `test_client` → `/health`, `/`, `/produtos` = 200; login seed OK; `/admin/query` = 403
- **P2:** checkout card `4111…` = 200; financial-report consistente; DELETE user limpa FKs
- **P3:** `/health`, `/`, `/tasks`, `/users`, `/reports/summary`, `/categories` = 200; login sem password no JSON

### Observação multi-stack

A mesma skill detectou God Class no Express e Fat Routes no Flask parcial; o playbook guiou rebuild completo (P1/P2) vs realinhamento (P3) sem duplicar a skill.

---

## D) Como Executar

### Pré-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) instalado e autenticado
- Python 3.10+ (projetos 1 e 3)
- Node.js 18+ (projeto 2)

### Executar a skill

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"
# Confirmar Phase 3 com: y

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 em `reports/audit-project-{1,2,3}.md` (já presentes neste fork).

### Validar aplicações refatoradas

```bash
# Projeto 1
cd code-smells-project
pip install -r requirements.txt
python app.py
# curl http://localhost:5000/health

# Projeto 2
cd ../ecommerce-api-legacy
npm install && npm start
# usar api.http ou curl :3000/api/checkout

# Projeto 3
cd ../task-manager-api
pip install -r requirements.txt
python seed.py && python app.py
# curl http://localhost:5000/tasks
```

### Ordem sugerida

1. Análise manual (seção A)  
2. Criar/ajustar skill em `code-smells-project`  
3. Rodar nos 3 projetos (iterar refs se preciso)  
4. Commitar código + reports + README  

---

## Estrutura do repositório

```
mba-ia-refactor-projects-skill/
├── README.md
├── docs/                          # RPI Research + Plan
├── reports/
│   ├── audit-project-1.md
│   ├── audit-project-2.md
│   └── audit-project-3.md
├── code-smells-project/
│   └── .claude/skills/refactor-arch/
├── ecommerce-api-legacy/
│   └── .claude/skills/refactor-arch/
└── task-manager-api/
    └── .claude/skills/refactor-arch/
```
