================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0 + SQLAlchemy
Files:   15 analyzed | ~900 lines of code

## Summary
CRITICAL: 1 | HIGH: 3 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Sensitive Data Exposure
File: models/user.py:21
Description: `to_dict()` inclui o hash de senha; login/create devolvem user serializado com password.
Impact: Vazamento de hashes facilita offline cracking.
Recommendation: Remover password do serializer público (playbook #9).

### [HIGH] Weak / Fake Authentication
File: models/user.py:29-32, routes/user_routes.py:185-211
Description: Hash MD5; token `fake-jwt-token-{id}` sem middleware de verificação nas rotas.
Impact: Autenticação nominal sem proteção real.
Recommendation: SHA-256+ (bcrypt em produção); preparar auth middleware (playbook #7).

### [HIGH] Fat Controller / Business in Routes
File: routes/task_routes.py:11-154
Description: Rotas concentram validação, serialização, overdue e queries.
Impact: Duplicação e violação MVC apesar das pastas models/routes.
Recommendation: Extrair controllers; routes finas (playbook #4).

### [HIGH] N+1 Queries
File: routes/task_routes.py:11-59
Description: GET /tasks faz User.query.get e Category.query.get por item.
Impact: Performance degrada com volume de tasks.
Recommendation: joinedload / eager load (playbook #6).

### [MEDIUM] Deprecated / Legacy APIs
File: models/user.py, models/task.py, routes/*.py
Description: Uso de `datetime.utcnow()` (deprecated 3.12+) e `Model.query.get` (legado SQLAlchemy 2.0).
Impact: Warnings/quebra futura em runtimes novos.
Recommendation: `datetime.now(timezone.utc)` e `db.session.get` (playbook #7).

### [MEDIUM] Wrong bounded context / dead code
File: routes/report_routes.py:157-223, services/notification_service.py:1-48
Description: CRUD de categories no blueprint de reports; NotificationService nunca importado e com SMTP hardcoded.
Impact: Arquitetura confusa; secret morto no repo.
Recommendation: Category routes dedicadas; remover ou sanitizar service (playbook #8).

### [MEDIUM] Bare except swallowing errors
File: routes/task_routes.py:62-63
Description: `except:` genérico retorna 500 sem log.
Impact: Falhas silenciosas; diagnóstico difícil.
Recommendation: Error handler centralizado (playbook #5).

### [LOW] Hardcoded SECRET_KEY
File: app.py:12-13
Description: SECRET_KEY literal no composition root.
Impact: Risco se o binário/repo vazar.
Recommendation: config/settings via env (playbook #1).

### [LOW] Unused dependencies / magic
File: requirements.txt:1-6
Description: marshmallow e requests declarados mas não usados.
Impact: Superfície e ruído de dependências.
Recommendation: Remover deps mortas (playbook #8).

================================
Total: 9 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
