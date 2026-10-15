# 02 — Como escrever Skills (boas práticas)

Fontes:

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic Engineering)
- Princípios de authoring (progressive disclosure, concisão, workflows)

## Anatomia de uma skill

Uma skill é um **diretório** com:

1. `SKILL.md` — obrigatório
2. Arquivos de referência Markdown (e, opcionalmente, scripts) — progressive disclosure

### Frontmatter YAML

Campos essenciais:

```yaml
---
name: refactor-arch
description: Analisa, audita e refatora backends para MVC. Use quando o usuário invocar /refactor-arch ou pedir refatoração arquitetural automatizada.
disable-model-invocation: true
---
```

| Campo | Papel |
|-------|--------|
| `name` | Identificador / comando (`/refactor-arch`) |
| `description` | WHAT + WHEN; ajuda o agente a decidir se carrega a skill |
| `disable-model-invocation: true` | Skill só sobe quando o usuário invoca `/refactor-arch` — adequado a fluxos longos e destrutivos |

Para esta skill: **sempre** `disable-model-invocation: true` (refatoração não deve disparar sozinha).

### Progressive disclosure (3 níveis)

1. **Metadata** (`name` + `description`) — pré-carregada no system prompt
2. **Body do `SKILL.md`** — carregado ao invocar a skill
3. **Arquivos linkados** — o agente lê sob demanda quando a fase exige

Implicação: manter `SKILL.md` **enxuto** (workflow + gates + links). Catálogo grande, playbook e templates ficam em refs.

Regra: links **um nível** a partir do `SKILL.md` (evitar cadeias profundas de referências).

## Onde instalar no desafio

| Tipo | Path |
|------|------|
| Project skill (por app) | `{projeto}/.claude/skills/refactor-arch/` |

O enunciado exige a skill **dentro de cada um dos 3 projetos** e cópia da pasta para projetos 2 e 3. Claude Code carrega skills do diretório atual e pais; ao `cd code-smells-project` e rodar `claude`, a skill nested fica disponível.

## Princípios de authoring

### 1. Concisão

O contexto compete com histórico e outras skills. Assumir que o modelo já é competente; incluir só o que ele **não** tem (sinais de detecção, template exato, gates, playbook concreto).

### 2. Sinais acionáveis

Ruim: “código ruim”, “melhorar arquitetura”.

Bom: “query SQL concatenada com input do usuário dentro de `execute(...)` → CRITICAL SQL Injection; citar arquivo:linha”.

### 3. Graus de liberdade

| Nível | Uso nesta skill |
|-------|-----------------|
| Alto | Julgamento de domínio / stack (Fase 1) |
| Médio | Relatório e mapeamento para MVC |
| Baixo | Gate de confirmação; checklist de validação Fase 3 |

### 4. Padrões recomendados

| Padrão | Aplicação em `refactor-arch` |
|--------|------------------------------|
| **Workflow** | Fase 1 → 2 → 3 com checklist explícito |
| **Template** | Relatório de auditoria padronizado |
| **Conditional** | Monólito (rebuild MVC) vs parcialmente organizado (realinhar camadas) |
| **Feedback loop** | Após refatorar: boot → smoke endpoints → corrigir se falhar |

### 5. Agnosticismo de tecnologia

- Heurísticas por **manifestos** (`requirements.txt`, `package.json`, imports), não por nomes fixos dos 3 projetos
- Playbook por **anti-pattern → transformação de camada**, com exemplos Python **e** Node quando o smell existir em ambos
- Validação: descobrir comando de boot e lista de endpoints na Fase 1; não hardcodar só `/produtos`

### 6. Start with evaluation

Fluxo Anthropic alinhado ao desafio:

1. Rodar a skill nos 3 projetos
2. Observar gaps (poucos findings, refatoração quebrada, stack errada)
3. Ajustar refs (catálogo / playbook)
4. Reexecutar — esperado **2–4 iterações**

## Estrutura recomendada do `SKILL.md` (conceitual)

```markdown
---
name: refactor-arch
description: ...
disable-model-invocation: true
---

# Refactor Arch

## When invoked
Execute phases 1→2→3 in order. Do not skip gates.

## References (load as needed)
- Phase 1: [project-analysis.md](project-analysis.md)
- Phase 2: [anti-patterns.md](anti-patterns.md), [report-template.md](report-template.md)
- Phase 3: [mvc-architecture.md](mvc-architecture.md), [refactor-playbook.md](refactor-playbook.md)

## Phase 1 — Analysis
...

## Phase 2 — Audit
...
STOP and ask: Proceed with refactoring (Phase 3)? [y/n]
Zero file modifications before explicit "y".

## Phase 3 — Refactor + Validate
...
```

## Segurança e confiança

Skills podem instruir o agente a alterar o filesystem. Para o desafio:

- Fase 2 **sem writes** até confirmação humana
- Não embutir scripts que exfiltrem dados
- Skill commitada no repo = auditável pelo avaliador

## Anti-padrões de skill (evitar)

| Evitar | Preferir |
|--------|----------|
| `SKILL.md` com 1000+ linhas de catálogo | Catálogo em `anti-patterns.md` |
| Paths hardcoded (`somente models.py`) | Heurísticas + glob de source |
| Refatorar sem confirmação | Gate `[y/n]` obrigatório |
| Um único exemplo só em Flask | Exemplos dual-stack no playbook |
| “Zero anti-patterns” sem validar | Boot + smoke real |

## Checklist de qualidade da skill (antes de considerar “pronta”)

- [ ] Frontmatter com `name: refactor-arch` e description clara
- [ ] `disable-model-invocation: true`
- [ ] 3 fases explícitas + gate de confirmação
- [ ] 5 refs cobrindo as 5 áreas obrigatórias
- [ ] Catálogo ≥ 8 com severidades distribuídas + deprecated APIs
- [ ] Playbook ≥ 8 transformações before/after
- [ ] Copiável: mesma pasta funciona nos 3 projetos sem edição por projeto
- [ ] Avaliada pelo menos uma vez em cada stack

## Próximo doc

Landscape dos projetos que a skill deve cobrir → [`03-projects-landscape.md`](./03-projects-landscape.md)
