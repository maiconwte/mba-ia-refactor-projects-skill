================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 3 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] God Class / God Module
File: models.py:1-314
Description: Arquivo único concentra SQL, regras de pedidos, relatórios e busca para múltiplos domínios (produtos, usuários, pedidos).
Impact: Impossível testar ou alterar um domínio sem risco colateral.
Recommendation: Separar models/controllers por domínio (playbook #2).

### [CRITICAL] Hardcoded Credentials / Secrets
File: app.py:7-8
Description: SECRET_KEY literal 'minha-chave-super-secreta-123' e DEBUG=True no source.
Impact: Compromete sessões e exposição de debug em deploy.
Recommendation: Extrair para config/settings via variáveis de ambiente (playbook #1).

### [CRITICAL] SQL Injection / Arbitrary Client Query
File: app.py:59-78
Description: POST /admin/query executa SQL arbitrário do body (`cursor.execute(query)`).
Impact: Compromisso total do banco.
Recommendation: Remover ou bloquear endpoint; nunca executar SQL do cliente (playbook #3).

### [CRITICAL] Sensitive Data Exposure
File: models.py:72-87
Description: Senhas em plaintext no banco; listagem de usuários retorna campo senha.
Impact: Vazamento de credenciais e takeover de contas.
Recommendation: Hash de senha + serializer público sem senha (playbook #9).

### [HIGH] SQL Injection in search/login
File: models.py:109-110, models.py:285-299
Description: Login e busca concatenam input do usuário em strings SQL.
Impact: Bypass de autenticação e leitura/alteração de dados.
Recommendation: Queries parametrizadas (playbook #3).

### [HIGH] Unauthenticated destructive admin
File: app.py:47-57
Description: POST /admin/reset-db apaga todas as tabelas sem autenticação.
Impact: Denial of service / perda de dados.
Recommendation: Proteger com token admin via env (playbook #7 / #1).

### [HIGH] N+1 Queries
File: models.py:171-233
Description: Listagem de pedidos abre cursors aninhados por pedido/item.
Impact: Latência cresce com volume de pedidos.
Recommendation: Joins ou fetch agregado (playbook #6).

### [MEDIUM] Fat Controller / duplicated validation
File: controllers.py:24-96
Description: Validação de produto e side effects (print de email/SMS) no controller HTTP.
Impact: Dificulta reuso e testes.
Recommendation: Mover orquestração limpa para controllers de domínio; side effects explícitos (playbook #4).

### [MEDIUM] Global Mutable State
File: database.py:7-10
Description: Singleton global `db_connection` com `check_same_thread=False`.
Impact: Acoplamento e risco de concorrência.
Recommendation: Ciclo de vida explícito no composition root (playbook #10).

### [LOW] Health endpoint claims production while leaking internals
File: controllers.py:264-292
Description: Health reporta ambiente "producao", debug true e secret_key.
Impact: Information disclosure.
Recommendation: Health mínimo sem secrets (playbook #9).

### [LOW] Magic / debug defaults
File: app.py:88
Description: `app.run(..., debug=True)` fixo no entrypoint.
Impact: Comportamento inseguro se implantado sem mudança.
Recommendation: Controlar via env DEBUG (playbook #1).

================================
Total: 11 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
