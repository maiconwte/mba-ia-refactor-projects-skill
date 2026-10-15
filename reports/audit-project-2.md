================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express 4.18
Files:   3 analyzed | ~180 lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] God Class / God Module
File: src/AppManager.js:1-141
Description: Classe única inicializa schema, seed e todos os handlers HTTP (checkout, report, delete).
Impact: Qualquer mudança toca o núcleo inteiro da aplicação.
Recommendation: Separar models, controllers e routes (playbook #2).

### [CRITICAL] Hardcoded Credentials / Secrets
File: src/utils.js:1-7
Description: dbPass, paymentGatewayKey e smtpUser literais no source.
Impact: Vazamento de credenciais de infraestrutura e pagamento.
Recommendation: process.env via config/settings (playbook #1).

### [HIGH] Sensitive Data Exposure
File: src/AppManager.js:45
Description: Loga número completo do cartão e chave do gateway no console.
Impact: Violação de dados de pagamento (PCI-like).
Recommendation: Nunca logar PAN/chave; mascarar cartão (playbook #9).

### [HIGH] Fat Controller / Business in Routes
File: src/AppManager.js:28-78
Description: Checkout executa registro, pagamento mock, enrollment e audit em callbacks aninhados.
Impact: Fluxo frágil, difícil de testar e estender.
Recommendation: CheckoutController + models (playbook #4).

### [HIGH] Weak / Fake Authentication
File: src/utils.js:17-23, src/AppManager.js:18
Description: badCrypto fraco; seed com senha '123'; rotas admin sem auth.
Impact: Credenciais triviais e admin aberto.
Recommendation: SHA-256+ (idealmente bcrypt) e proteger admin (playbook #7).

### [MEDIUM] N+1 / race in financial report
File: src/AppManager.js:80-129
Description: forEach assíncrono monta report com contadores — race e resultados incompletos.
Impact: Relatório financeiro incorreto.
Recommendation: Aguardar queries sequencialmente/Promise.all estruturado (playbook #6).

### [MEDIUM] Orphan data on DELETE user
File: src/AppManager.js:131-137
Description: DELETE remove só o user; admite orphans em enrollments/payments.
Impact: Integridade referencial quebrada.
Recommendation: Cascade explícito nas related tables (playbook #2/#8).

### [LOW] Cryptic naming / magic fields
File: src/AppManager.js:29-33
Description: Body usa usr, eml, pwd, c_id, cc sem validação de schema.
Impact: DX ruim; erros silenciosos.
Recommendation: Nomes claros ou validação documentada (playbook #8 naming); manter contrato se necessário.

### [LOW] Deprecated / Legacy APIs
File: src/AppManager.js:28-78
Description: API sqlite3 baseada só em callbacks profundos; sem routers Express.
Impact: Manutenção difícil; padrões legados.
Recommendation: Promisify/async models + express.Router (playbook #7).

================================
Total: 9 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
