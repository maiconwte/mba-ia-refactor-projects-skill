# Project Analysis Heuristics

Use these signals to detect stack and architecture. Prefer reading manifests and entrypoints first.

## Language

| Language | Signals |
|----------|---------|
| Python | `*.py`, `requirements.txt`, `pyproject.toml`, `Pipfile` |
| JavaScript / Node | `package.json`, `*.js`, `*.mjs`, `*.cjs` |
| TypeScript | `tsconfig.json`, `*.ts`, dependencies on `typescript` |

## Framework

| Framework | Signals |
|-----------|---------|
| Flask | `from flask import`, `Flask(`, `flask` in requirements |
| Express | `require('express')`, `from 'express'`, `express` in `package.json` |
| FastAPI | `from fastapi import`, `FastAPI(` |
| NestJS / other | `package.json` deps + framework imports |

Also record framework version from lockfile/manifest when available.

## Dependencies

- Python: parse `requirements.txt` / `pyproject.toml`
- Node: parse `dependencies` + `devDependencies` in `package.json`
- Note unused declared deps if never imported (quality signal for Phase 2)

## Database

| DB access | Signals |
|-----------|---------|
| SQLite file | `sqlite3.connect('*.db')`, `sqlite:///`, `*.db` files |
| SQLite memory | `:memory:` |
| SQLAlchemy | `SQLAlchemy`, `flask_sqlalchemy`, `db.Model` |
| Raw SQL | string queries with `SELECT`/`INSERT` passed to `execute` |
| Tables | `CREATE TABLE`, ORM model `__tablename__`, seed inserts |

## Domain

Infer from:

- README title/description
- Route path names (`/produtos`, `/tasks`, `/api/checkout`)
- Model / table names
- Seed data labels

Write a one-line domain summary, e.g. `E-commerce API (products, orders, users)`.

## Architecture style

| Style | Signals |
|-------|---------|
| **flat / monolithic** | Few source files at root; logic mixed across 2–5 modules |
| **god-class** | One file/class owns schema + routes + business rules |
| **partial layers** | Folders like `models/`, `routes/`, `services/` exist but responsibilities leak |
| **MVC-like** | Clear models + views/routes + controllers with thin boundaries |

Count analyzable source files (exclude vendor, caches, lockfiles, binaries).

## Phase 1 output template

Print exactly this shape (fill values):

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <language>
Framework:     <framework + version if known>
Dependencies:  <key deps>
Domain:        <one-line domain>
Architecture:  <flat | god-class | partial layers | ...> — <short note>
Source files:  <N> files analyzed
DB tables:     <comma-separated or n/a>
================================
```
