# refactor-arch Skill

## Objetivo

Esta skill automatiza a análise, auditoria e refatoração de projetos backend legados para o padrão MVC. Ela deve ser usada em projetos Python/Flask e Node.js/Express e deve seguir 3 fases sequenciais:

1. **Análise de Projeto**
2. **Auditoria de Anti-Patterns**
3. **Refatoração para MVC + Validação**

## Estrutura de conhecimento

A skill deve usar os arquivos de referência abaixo para guiar cada fase:

- `analysis-heuristics.md`
- `anti-patterns-catalog.md`
- `audit-report-template.md`
- `mvc-guidelines.md`
- `refactor-playbook.md`

## Instruções de execução

### Fase 1 — Análise

1. Percorra o código-fonte buscando sinais de linguagem e framework.
2. Detecte o stack principal (por exemplo, Python + Flask ou Node.js + Express).
3. Identifique o banco de dados ou mecanismo de persistência e qualquer uso de consultas SQL diretas.
4. Classifique a arquitetura atual como monolítica, parcialmente modularizada ou organizada em camadas.
5. Liste o conjunto de arquivos analisados, as dependências principais e os domínios funcionais do projeto.

### Fase 2 — Auditoria

1. Use o catálogo de anti-patterns para identificar problemas no código.
2. Gere um relatório de auditoria seguindo o template padrão.
3. Classifique cada achado com severidade (CRITICAL, HIGH, MEDIUM, LOW).
4. Indique arquivo e linha aproximada para cada finding.
5. Após listar os problemas, peça confirmação explícita antes de começar a refatoração.

> Exemplo de prompt de confirmação: `Continuar com a refatoração do projeto? Responda apenas com y ou n.`

### Fase 3 — Refatoração

1. Reestruture o projeto para o padrão MVC.
2. Extraia configuração e segredos para um módulo de config separado.
3. Separe models, controllers/serviços e views/routes de acordo com o stack.
4. Centralize tratamento de erros e normalize respostas JSON.
5. Preserve os endpoints originais e o comportamento funcional da aplicação.
6. Valide a aplicação iniciando-a e conferindo os endpoints básicos de saúde e de recursos principais.

## Regras de comportamento

- A skill deve ser agnóstica de tecnologia e funcionar em Python/Flask e Node.js/Express.
- A skill deve suportar projetos completamente monolíticos e projetos com alguma organização existente.
- A Fase 2 deve sempre pausar e aguardar confirmação antes de alterar qualquer arquivo.
- A Fase 3 deve incluir validação de boot e checagem de endpoint mínimo (`/health`, `/`, rotas principais).
- O relatório de auditoria deve ser salvo em `reports/audit-project-<n>.md` se a skill suportar saída de arquivo.

## Indicações de uso com Gemini CLI

- Coloque esta skill em `.gemini/skills/refactor-arch/`.
- Adapte o comando de invocação ao seu ambiente Gemini CLI.
- Se o runtime permitir, utilize `gemini --skill refactor-arch` ou equivalente.

## Resultado esperado

No final da execução desta skill, deve existir:

- Um relatório de auditoria estruturado com findings e recomendações
- Uma proposta de refatoração para MVC
- Um projeto reorganizado com models, controllers/serviços e routes/views separados
- Uma validação que confirma que a aplicação inicializa e responde ao menos aos endpoints principais
