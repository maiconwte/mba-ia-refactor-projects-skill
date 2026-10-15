# 01 — O que DEVE ser feito (requisitos de aceitação)

Fonte primária: [`README.md`](../../README.md) do repositório do desafio.

## Objetivo da skill

Entregar uma skill **agnóstica de tecnologia** capaz de:

1. Analisar uma codebase (linguagem, framework, arquitetura atual)
2. Identificar anti-patterns / code smells com severidade e **arquivo + linha exatos**
3. Gerar relatório de auditoria estruturado
4. Refatorar para o padrão **MVC** (Model–View–Controller)
5. Validar que a aplicação continua funcionando (boot + endpoints)

## Entregáveis obrigatórios

| Entregável | Local |
|------------|-------|
| Skill completa | `.claude/skills/refactor-arch/` **dentro de cada um dos 3 projetos** |
| Código refatorado (Fase 3) | Commitado em cada projeto |
| Relatórios de auditoria (saída Fase 2) | `reports/audit-project-1.md`, `audit-project-2.md`, `audit-project-3.md` (raiz do repo) |
| README atualizado | Seções Análise Manual, Construção da Skill, Resultados, Como Executar |

## Skill — restrições imutáveis

| Item | Valor |
|------|-------|
| Nome da skill | `refactor-arch` (não alterar) |
| Arquivo principal | `SKILL.md` (não alterar o nome) |
| Path (Claude Code) | `.claude/skills/refactor-arch/` |
| Formato dos refs | Markdown |
| Ferramenta | Claude Code (fixada no Research) |

### Três fases sequenciais

| Fase | Nome | Obrigatório |
|------|------|-------------|
| 1 | Análise | Detectar stack, mapear arquitetura, imprimir resumo |
| 2 | Auditoria | Cruzar código × catálogo, gerar relatório, **pedir confirmação** antes de qualquer escrita |
| 3 | Refatoração | Reestruturar para MVC, **validar** boot + endpoints |

### Cinco áreas de conhecimento (arquivos de referência)

Todas devem estar cobertas (nomes livres; conteúdo obrigatório):

1. **Análise de projeto** — heurísticas de linguagem, framework, banco, mapeamento de arquitetura
2. **Catálogo de anti-patterns** — ≥ **8** anti-patterns; severidades CRITICAL / HIGH / MEDIUM / LOW; incluir **APIs deprecated**
3. **Template de relatório** — formato padronizado da Fase 2
4. **Guidelines de arquitetura** — regras MVC alvo (Models, Views/Routes, Controllers)
5. **Playbook de refatoração** — ≥ **8** padrões de transformação com exemplos before/after

### Requisitos comportamentais da skill

- Agnóstica: funcionar nos 3 projetos (2× Python/Flask com níveis diferentes + 1× Node/Express)
- Fase 2 **pausa** e pede confirmação antes de modificar arquivos
- Fase 3 **valida** resultado (aplicação sobe + endpoints respondem)

## Escala de severidade (obrigatória)

| Severidade | Critério (resumo) |
|------------|-------------------|
| **CRITICAL** | Arquitetura/segurança grave: credenciais hardcoded, SQL injection, God Class que mistura DB + lógica + roteamento |
| **HIGH** | Violações fortes de MVC/SOLID: business logic em controllers, acoplamento sem DI, estado global mutável |
| **MEDIUM** | Padronização, duplicação, performance moderada: N+1, middlewares inadequados, validações ausentes |
| **LOW** | Legibilidade, nomenclatura, magic numbers |

## Análise Manual (pré-requisito de entendimento)

Antes/paralelo à skill, documentar no README (≥5 problemas por projeto):

- ≥ 1 CRITICAL ou HIGH
- ≥ 2 MEDIUM
- ≥ 2 LOW

Usar os projetos como insumo para o catálogo — não precisa listar todos os smells existentes.

## Execução nos 3 projetos

| # | Projeto | Stack | Ação especial |
|---|---------|-------|---------------|
| 1 | `code-smells-project/` | Python/Flask | Criar skill aqui primeiro; `reports/audit-project-1.md` |
| 2 | `ecommerce-api-legacy/` | Node/Express | **Copiar** a skill; `reports/audit-project-2.md` |
| 3 | `task-manager-api/` | Python/Flask (camadas parciais) | **Copiar** a skill; melhorar sem quebrar; `reports/audit-project-3.md` |

Para cada um: Fase 1 OK → Fase 2 ≥5 findings (idealmente alinhados à análise manual) → confirmar → Fase 3 MVC + validação → commit.

### Projeto 3 — nuance

Já tem models/routes/services/utils. A skill deve detectar problemas de segurança/performance/qualidade **e** oportunidades arquiteturais; adaptar a Fase 3 (não forçar o mesmo rebuild de um monólito).

## Critérios de aceite (todos 3/3 projetos)

| Critério | Obrigatório |
|----------|-------------|
| Fase 1 detecta stack corretamente | Sim (3/3) |
| Fase 2 encontra ≥ 5 findings | Sim (3/3) |
| Fase 2 inclui ≥ 1 CRITICAL ou HIGH | Sim (3/3) |
| Fase 3 aplicação funciona após refatoração | Sim (3/3) |

“Funciona” = API inicia sem erros e endpoints originais continuam respondendo.

## Checklist de validação (por projeto)

### Fase 1

- [ ] Linguagem correta
- [ ] Framework correto
- [ ] Domínio descrito corretamente
- [ ] Número de arquivos analisados coerente

### Fase 2

- [ ] Relatório segue o template dos refs
- [ ] Cada finding com arquivo e linhas exatos
- [ ] Ordenado CRITICAL → LOW
- [ ] ≥ 5 findings
- [ ] Detecção de APIs deprecated (se aplicável)
- [ ] Pausa pedindo confirmação antes da Fase 3

### Fase 3

- [ ] Estrutura MVC
- [ ] Config extraída (sem hardcoded)
- [ ] Models abstraindo dados
- [ ] Views/Routes separadas
- [ ] Controllers no fluxo
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Boot sem erros
- [ ] Endpoints originais OK

## README final — seções obrigatórias

- **A) Análise Manual** — problemas por projeto, severidade, justificativa
- **B) Construção da Skill** — design, catálogo, agnosticismo, desafios
- **C) Resultados** — totais por severidade, before/after, checklist, logs/screenshots, observação multi-stack
- **D) Como Executar** — pré-requisitos, comandos, validação, ordem sugerida

## Fora deste doc

Como *escrever* a skill (boas práticas) → [`02-skills-best-practices.md`](./02-skills-best-practices.md)  
Landscape dos projetos → [`03-projects-landscape.md`](./03-projects-landscape.md)  
Decisões de design → [`04-skill-design-implications.md`](./04-skill-design-implications.md)
