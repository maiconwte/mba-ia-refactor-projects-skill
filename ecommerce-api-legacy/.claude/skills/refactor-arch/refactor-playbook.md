# Refactor Playbook (≥8 transformations)

Each pattern: problem → target. Adapt syntax to the detected stack.

---

## 1. Extract configuration / secrets

**Before (Python):**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

**After:**
```python
# config/settings.py
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
```

**Before (Node):**
```js
module.exports = { dbPass: "root123", paymentGatewayKey: "pk_live_..." };
```

**After:**
```js
// config/settings.js
module.exports = {
  port: process.env.PORT || 3000,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "pk_test_dummy",
};
```

---

## 2. Split God Class → MVC by domain

**Before:** one `AppManager` / mega `models.py` with users+orders+reports.

**After:**
- `models/user_model.*`, `models/order_model.*`
- `controllers/user_controller.*`, `controllers/order_controller.*`
- `views/routes.*` only registers endpoints

---

## 3. Parameterize SQL / remove arbitrary client SQL

**Before:**
```python
cursor.execute(f"SELECT * FROM usuarios WHERE email = '{email}'")
cursor.execute(request.json["query"])  # admin
```

**After:**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
# delete arbitrary SQL endpoint or require strong admin auth + allowlist
```

---

## 4. Move business logic from routes → controllers

**Before (Express):**
```js
app.post("/api/checkout", (req, res) => {
  // validate + create user + charge card + enroll + audit in one callback
});
```

**After:**
```js
// routes
router.post("/api/checkout", (req, res, next) =>
  checkoutController.checkout(req, res, next)
);
// controllers/checkoutController.js orchestrates models
```

---

## 5. Centralize error handling

**Before:**
```python
except:
    return jsonify({"erro": "Erro"}), 500
```

**After:**
```python
# middlewares/error_handler.py
@app.errorhandler(Exception)
def handle_error(err):
    # map domain errors; log unexpected
    return jsonify({"error": str(err)}), getattr(err, "code", 500)
```

**Node:**
```js
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message });
});
```

---

## 6. Fix N+1 queries

**Before:**
```python
for order in orders:
    items = db.execute("SELECT * FROM itens WHERE pedido_id = ?", (order["id"],))
```

**After:** join or fetch related rows in one query / use eager load:

```python
# SQLAlchemy
Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
```

---

## 7. Replace deprecated / legacy APIs

**Before:**
```python
from datetime import datetime
now = datetime.utcnow()
user = User.query.get(id)
```

**After:**
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
user = db.session.get(User, id)
```

**Node sqlite callbacks → promisified wrapper or async API** so controllers stay linear.

---

## 8. Remove dead code / fix bounded contexts

**Before:** `NotificationService` never imported; category CRUD registered on `report` blueprint.

**After:** delete or wire the service intentionally; move category routes to `category` routes/controller.

---

## 9. Fix password hashing and stop leaking secrets

**Before:**
```python
# plaintext or MD5
usuario["senha"]  # returned in API
```

**After:**
```python
import hashlib
def hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()  # prefer bcrypt in real apps

def to_public_dict(user):
    return {"id": user.id, "email": user.email}  # never password
```

Never log payment card numbers.

---

## 10. Thin composition-root entrypoint

**Before:** `app.py` defines routes, SQL admin tools, and business side effects.

**After:**
```python
from flask import Flask
from config.settings import SECRET_KEY, DEBUG
from views.routes import register_routes
from middlewares.error_handler import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    register_error_handlers(app)
    register_routes(app)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
```

---

## Phase 3 completion output

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<tree>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Critical anti-patterns addressed
================================
```
