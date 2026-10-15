# MVC Architecture Guidelines (Target)

Apply these layer rules regardless of language. Adapt folder names to stack conventions.

## Layer responsibilities

| Layer | Responsibility | Must NOT |
|-------|----------------|----------|
| **Config** | Load settings from environment; app constants | Hardcode secrets; run SQL; handle HTTP |
| **Models** | Data access, persistence, entity rules close to data | Parse HTTP requests; choose status codes; render responses |
| **Views / Routes** | Map HTTP methods/paths to controllers; parse input; return responses | Own business workflows; embed complex SQL |
| **Controllers** | Orchestrate use cases; call models; shape results/errors for routes | Talk to raw sockets; own framework app bootstrap |
| **Middlewares** | Cross-cutting: errors, auth, logging, CORS | Domain-specific business rules |
| **Entry / Composition root** | Create app, wire dependencies, register routes | Fat business logic |

## Target structures

### Python / Flask (illustrative)

```
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py          # or blueprints under views/
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/
│   └── error_handler.py
└── app.py                 # composition root
```

Keeping `app.py` at project root is acceptable if it only wires modules.

### Node / Express (illustrative)

```
src/
├── config/settings.js
├── models/
├── controllers/
├── views/                 # or routes/
│   └── routes.js
├── middlewares/
│   └── errorHandler.js
└── app.js                 # composition root
```

## Adaptive strategy

| Detected architecture | Phase 3 approach |
|-----------------------|------------------|
| flat / monolithic / god-class | Create MVC folders; move code by responsibility; thin entrypoint |
| partial layers | Keep ORM/blueprints if sound; extract fat route logic into controllers; add config + error middleware; remove dead code; fix security/N+1 |

## Endpoint contracts

- Preserve existing public paths and methods when possible.
- CRITICAL insecure endpoints (arbitrary SQL, unauthenticated DB reset) may be **removed** or **auth-gated**; document in Phase 3 summary.
- Keep response JSON shapes stable enough for smoke tests unless fixing a security leak (e.g. stop returning passwords).

## Error handling

- One centralized handler mapping domain errors → HTTP status + JSON `{ "error": "..." }`.
- Avoid bare `except:` / empty catch that swallows errors.

## Configuration

- `SECRET_KEY`, DB URLs, SMTP, payment keys → environment with safe defaults only for local demo.
- Never commit real production secrets.
