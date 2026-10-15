# Anti-Pattern Catalog

Scan source against each entry. Record file path and exact line ranges. Severity scale: CRITICAL > HIGH > MEDIUM > LOW.

Minimum: report all matches found; aim for ≥5 findings when smells exist; always include CRITICAL/HIGH when present.

---

## 1. God Class / God Module

**Severity:** CRITICAL

**Detection signals:**
- Single file/class defines DB schema, HTTP routes, and business rules together
- File > ~200 LOC with multiple unrelated domains (users + payments + reports)
- Class named `*Manager` / `App*` that registers all routes and runs SQL

**Impact:** Impossible to test or change one concern without risking others.

**Recommendation:** Split into models, controllers, and routes/views per domain.

---

## 2. Hardcoded Credentials / Secrets

**Severity:** CRITICAL

**Detection signals:**
- Literals: `SECRET_KEY`, `password`, `apiKey`, `paymentGateway`, SMTP credentials in source
- Strings like `minha-chave`, `dbPass`, tokens committed in repo
- Config objects with production-like secrets at module top-level

**Impact:** Credential leak; compromised environments.

**Recommendation:** Move to environment variables / config module reading `os.environ` / `process.env`.

---

## 3. SQL Injection / Arbitrary Client Query

**Severity:** CRITICAL

**Detection signals:**
- SQL built with f-strings, `+`, or `.format()` including request input
- `execute(query)` where `query` comes from HTTP body/querystring
- Admin endpoints that run raw client SQL

**Impact:** Full database compromise.

**Recommendation:** Parameterized queries only; remove arbitrary SQL execution endpoints.

---

## 4. Sensitive Data Exposure

**Severity:** CRITICAL or HIGH

**Detection signals:**
- Password or password hash included in JSON/dict serializers (`to_dict`, API responses)
- Logging credit cards, CVV, or payment keys
- Health/debug endpoints returning `secret_key`, stack internals, or `debug: true` as “production” status
- Plaintext password storage/comparison

**Impact:** Account takeover, PCI/privacy violations.

**Recommendation:** Strip secrets from serializers; hash passwords with strong algorithms; never log payment data.

---

## 5. Fat Controller / Business Logic in Routes

**Severity:** HIGH

**Detection signals:**
- Route handlers with multi-step business workflows (validate + price + persist + notify)
- Duplicated domain rules across create/update handlers
- ORM/SQL queries embedded directly in route callbacks beyond trivial CRUD

**Impact:** Hard to reuse and unit-test; MVC boundary broken.

**Recommendation:** Move orchestration to controllers; keep routes as HTTP adapters.

---

## 6. Global Mutable State / Missing Dependency Injection

**Severity:** HIGH

**Detection signals:**
- Module-level mutable singletons (`db_connection = None`, `globalCache = {}`)
- Shared connection with `check_same_thread=False` without lifecycle management
- Controllers importing and mutating global config/state

**Impact:** Race conditions, hidden coupling, untestable modules.

**Recommendation:** Explicit composition root; inject DB/session; avoid globals.

---

## 7. Weak / Fake Authentication

**Severity:** HIGH

**Detection signals:**
- MD5/SHA1 for passwords; custom “badCrypto”; passwords like `'123'` in seeds used as production pattern
- Tokens like `fake-jwt-token-{id}` with no verification middleware
- Admin/destructive routes without auth checks

**Impact:** Trivial impersonation and privilege escalation.

**Recommendation:** Strong password hashing (bcrypt/argon2); real auth middleware; protect admin routes.

---

## 8. N+1 Queries

**Severity:** MEDIUM

**Detection signals:**
- Query inside `for`/`forEach` over collections
- Nested cursors (`cursor2`, `cursor3`) per parent row
- Per-item `Model.query.get` / `User.query.get` while serializing lists
- Loading all rows then filtering in Python for aggregates

**Impact:** Latency grows with dataset size.

**Recommendation:** Joins, eager loading, or single aggregated query.

---

## 9. Deprecated / Legacy APIs

**Severity:** MEDIUM (LOW if cosmetic only)

**Detection signals (examples):**
- Python: `datetime.utcnow()` → prefer `datetime.now(timezone.utc)`
- SQLAlchemy: `Model.query.get(id)` → prefer `db.session.get(Model, id)`
- Flask-SQLAlchemy: relying on `SQLALCHEMY_TRACK_MODIFICATIONS` (legacy no-op)
- Node sqlite3: deep nested callbacks without promisify / modern driver
- Express apps with no router split still using ad-hoc `app.post` everywhere in one class (legacy structure smell)

**Impact:** Breakage on newer runtimes; harder maintenance.

**Recommendation:** Replace with modern equivalents listed above; document migration in refactor.

---

## 10. Magic Numbers / Cryptic Naming / Dead Code

**Severity:** LOW

**Detection signals:**
- Unexplained numeric literals (ports, limits, status codes) without named constants
- Cryptic request fields (`usr`, `eml`, `pwd`, `c_id`, `cc`)
- Modules/services never imported; unused helpers; unused dependencies in manifest

**Impact:** Poor readability; confusion for maintainers.

**Recommendation:** Named constants, clear DTO field names, remove dead code/deps.

---

## Severity ranking for the report

When sorting findings: CRITICAL → HIGH → MEDIUM → LOW. If two share severity, list security before pure structure.
