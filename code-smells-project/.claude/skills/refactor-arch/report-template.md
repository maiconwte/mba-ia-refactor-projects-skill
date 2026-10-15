# Architecture Audit Report Template

Emit Phase 2 output in this exact structure (Markdown). Fill all placeholders. Do not invent findings without file:line evidence.

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <directory name>
Stack:   <Language + Framework>
Files:   <N> analyzed | ~<LOC> lines of code

## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

## Findings

### [CRITICAL] <Short title>
File: <path>:<start>-<end>
Description: <what is wrong>
Impact: <why it matters>
Recommendation: <how to fix / which playbook step>

### [HIGH] <Short title>
File: <path>:<start>-<end>
Description: ...
Impact: ...
Recommendation: ...

### [MEDIUM] <Short title>
File: <path>:<start>-<end>
Description: ...
Impact: ...
Recommendation: ...

### [LOW] <Short title>
File: <path>:<start>-<end>
Description: ...
Impact: ...
Recommendation: ...

================================
Total: <n> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Rules

1. Order findings CRITICAL → HIGH → MEDIUM → LOW.
2. Every finding must include `File: path:lines`.
3. Use catalog names from `anti-patterns.md` when they match.
4. Include at least one Deprecated / Legacy APIs finding when applicable.
5. Summary counts must match the listed findings.
6. After printing the report, **stop and wait** for `y`/`n`. No file modifications before `y`.
