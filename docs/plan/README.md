# Plan — Implementação da skill `refactor-arch`

Plano de implementação derivado do Research ([`../research/04-skill-design-implications.md`](../research/04-skill-design-implications.md)).

## Status

| Item | Status |
|------|--------|
| Plan documentado | Concluído |
| Implement | Pendente (após commit/push deste Plan + Research) |

## Documentos

| Doc | Conteúdo |
|-----|----------|
| [01-implementation-plan.md](./01-implementation-plan.md) | Ordem de trabalho, arquivos, conteúdo por artefato, execução e aceite |

## Premissas fixadas (não reabrir)

- Claude Code + `.claude/skills/refactor-arch/`
- Layout: `SKILL.md` + 5 refs Markdown
- Gate `[y/n]` antes de qualquer write na Fase 3
- Skill agnóstica; copiar a mesma pasta para os 3 projetos
- Target MVC com adaptação: rebuild (monólito) vs realinhamento (partial layers)
