# Docs — RPI da skill `refactor-arch`

Este diretório documenta o ciclo **Research → Plan → Implement** para a skill de refatoração arquitetural automatizada do desafio MBA IA.

## Status das fases

| Fase | Status | Artefatos |
|------|--------|-----------|
| Research | Concluída | [`research/`](./research/) |
| Plan | Concluída | [`plan/`](./plan/) |
| Implement | Concluída | `.claude/skills/refactor-arch/`, código MVC, `reports/` |

## Ferramenta fixada

- **Claude Code**
- Path da skill: `.claude/skills/refactor-arch/`
- Invocação: `claude "/refactor-arch"`
- Nome obrigatório: `refactor-arch` + arquivo `SKILL.md`

## Research

| Doc | Conteúdo |
|-----|----------|
| [01-requirements-must.md](./research/01-requirements-must.md) | O que **deve** ser entregue (aceitação, fases, severidades) |
| [02-skills-best-practices.md](./research/02-skills-best-practices.md) | Como **escrever** a skill (boas práticas Claude Code / Agent Skills) |
| [03-projects-landscape.md](./research/03-projects-landscape.md) | Landscape dos 3 projetos-alvo e smells evidenciados |
| [04-skill-design-implications.md](./research/04-skill-design-implications.md) | Implicações de design → input da fase Plan |

## Plan

| Doc | Conteúdo |
|-----|----------|
| [plan/README.md](./plan/README.md) | Índice da fase Plan |
| [01-implementation-plan.md](./plan/01-implementation-plan.md) | Ordem de trabalho, specs dos arquivos da skill, execução nos 3 projetos, DoD |

## Fluxo RPI

1. **Research** — requisitos, boas práticas, landscape, implicações
2. **Plan** — plano de implementação da skill e da execução nos 3 projetos
3. **Implement** — criar skill, análise manual, executar, reports, README final

## Próximo passo

Seguir [`plan/01-implementation-plan.md`](./plan/01-implementation-plan.md) na fase Implement (após commit/push de `docs/`).
