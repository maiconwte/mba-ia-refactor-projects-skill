---
name: refactor-arch
description: Analyzes a backend codebase, audits MVC/SOLID anti-patterns with severity, and refactors to MVC after human confirmation. Use when invoked as /refactor-arch or when the user requests automated architectural refactoring.
disable-model-invocation: true
---

# refactor-arch

Technology-agnostic architectural refactoring skill. Execute **Phase 1 → Phase 2 → Phase 3** in order. Do not skip gates. Do not modify any project files until the user explicitly confirms Phase 3 with `y`.

## References (load as needed)

- Phase 1: [project-analysis.md](project-analysis.md)
- Phase 2: [anti-patterns.md](anti-patterns.md), [report-template.md](report-template.md)
- Phase 3: [mvc-architecture.md](mvc-architecture.md), [refactor-playbook.md](refactor-playbook.md)

## Phase 1 — Project Analysis

1. Read [project-analysis.md](project-analysis.md).
2. Scan the current working directory (ignore `node_modules`, `.venv`, `__pycache__`, `.git`, `.claude`).
3. Detect language, framework, dependencies, domain, architecture style, source file count, and DB tables.
4. Print the summary using the Phase 1 template from `project-analysis.md`.
5. Proceed immediately to Phase 2.

## Phase 2 — Architecture Audit

1. Read [anti-patterns.md](anti-patterns.md) and [report-template.md](report-template.md).
2. Cross-check source code against the anti-pattern catalog.
3. For every finding, record exact file path and line range.
4. Produce the audit report following `report-template.md`.
5. Order findings CRITICAL → HIGH → MEDIUM → LOW.
6. Require at least 5 findings when anti-patterns are present; include at least one CRITICAL or HIGH when applicable.
7. Include deprecated/legacy API findings when present.
8. **STOP.** Ask exactly:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

9. **Do not create, edit, delete, or move any project files until the user answers `y`.**
10. If the user answers `n` (or anything other than `y`), stop without changes.

## Phase 3 — Refactor + Validate

Only after explicit `y`:

1. Read [mvc-architecture.md](mvc-architecture.md) and [refactor-playbook.md](refactor-playbook.md).
2. Choose strategy from Phase 1 architecture:
   - **flat / god-class / monolithic** → rebuild MVC structure while preserving endpoint contracts.
   - **partial layers** → realign layers (extract controllers, config, centralized errors); do not needlessly destroy working ORM/blueprints.
3. Apply playbook transformations for findings from Phase 2.
4. Extract configuration (no hardcoded secrets).
5. Ensure Models, Views/Routes, Controllers, centralized error handling, and a clear entry point.
6. Validate:
   - Install dependencies if needed.
   - Boot the application.
   - Smoke-test original endpoints (health/root + main domain routes; use `api.http` when present).
7. If validation fails, fix and re-validate (feedback loop).
8. Print the Phase 3 completion block (new structure + validation checklist).

## Hard rules

- Stay stack-agnostic: use heuristics from refs, never hardcode paths unique to one sample project.
- Preserve public HTTP contracts (methods + paths) unless a CRITICAL security endpoint must be removed or locked (document that change in the Phase 3 summary).
- Prefer small, coherent modules by domain over one giant file.
