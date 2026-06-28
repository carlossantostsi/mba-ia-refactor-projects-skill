# Skill de Refatoração Arquitetural para Projetos Legados

Este repositório entrega uma skill Gemini reutilizável para analisar, auditar e refatorar projetos backend legados para uma estrutura mais organizada, com foco em MVC, separação de responsabilidades e validação funcional.

Na minha maquina, utilizei uma versão do gemini cli, que precisou de um .sh para executar a skill
renomeie a pasta .gemini para poder versionar

A abordagem foi aplicada aos três projetos-alvo:

- [code-smells-project](code-smells-project) — Python + Flask
- [ecommerce-api-legacy](ecommerce-api-legacy) — Node.js + Express
- [task-manager-api](task-manager-api) — Python + Flask + SQLAlchemy

## A) Análise Manual

### 1. code-smells-project

- CRITICAL — God Class / God Method: o código concentrava lógica de negócio, acesso a banco, validação e formatação em poucos arquivos. Isso torna a manutenção difícil e aumenta o risco de regressões.
- CRITICAL — Credenciais hardcoded: o segredo da aplicação estava embutido no código, o que é um problema de segurança e de configuração por ambiente.
- HIGH — SQL injection: consultas SQL eram montadas por concatenação com valores externos, o que torna a aplicação vulnerável a exploração.
- HIGH — Lógica de negócio espalhada por controllers: rotas realizavam validação, regras de negócio e efeitos colaterais, o que quebra o princípio de responsabilidade única.
- HIGH — Endpoint administrativo inseguro: a rota de consulta SQL arbitrária expunha uma superfície de risco muito alta.
- MEDIUM — Duplicação de mapeamento de dados: várias funções repetiam a transformação de linhas do banco para dicionários.
- MEDIUM — Tratamento de erro inconsistente: alguns fluxos retornavam respostas diferentes para o mesmo tipo de falha.
- LOW — Strings mágicas e logs com print: dificultam a leitura e tornam o observability fraca.

### 2. ecommerce-api-legacy

- CRITICAL — Segredos hardcoded: valores sensíveis estavam no código-fonte, facilitando vazamento e dificultando separação entre ambientes.
- HIGH — Checkout com lógica de negócio no handler: a rota de checkout concentrava criação de usuário, processamento, auditoria e resposta em um único ponto.
- HIGH — Hash fraco de senha: a implementação usada não oferecia segurança adequada para autenticação.
- HIGH — Integridade de dados comprometida: a remoção de usuário deixava registros relacionados inconsistentes.
- MEDIUM — Payloads com chaves pouco intuitivas: os campos do body usavam nomes como usr, eml e c_id, o que gera ambiguidade e dificulta integração.
- MEDIUM — Estrutura antiga e callbacks aninhados: o código ficava difícil de evoluir e de testar.
- LOW — Valores mágicos e logging genérico: reduz a clareza do comportamento e dificulta manutenção.

### 3. task-manager-api

- HIGH — Lógica de negócio nas rotas: validações, cálculos e transformações estavam misturadas ao fluxo HTTP.
- HIGH — Hash MD5 para senha: inseguro para autenticação e incompatível com boas práticas de segurança.
- HIGH — Exposição de senha em respostas: os retornos de usuário incluíam dados sensíveis.
- MEDIUM — Cálculo de overdue duplicado: a mesma regra existia em vários pontos do código, gerando inconsistência.
- MEDIUM — Risco de N+1 queries: consultas repetidas dentro de loops podem degradar o desempenho.
- MEDIUM — Tratamento de erro genérico: as rotas capturavam exceções de forma ampla, o que prejudica diagnóstico e padronização.
- LOW — Strings mágicas e serialização duplicada: aumentam o custo de manutenção e o risco de divergência.

## B) Construção da Skill

### Decisões de design

- A skill foi organizada em 3 fases sequenciais: análise, auditoria e refatoração.
- A fase de auditoria sempre interrompe antes da alteração para garantir revisão humana.
- A refatoração foi concebida para preservar os endpoints públicos e o comportamento funcional das aplicações.
- A estrutura alvo foi baseada em camadas com configuração externa, controllers/serviços e rotas separadas.

### Anti-patterns incluídos na skill

A skill foi construída para reconhecer e orientar a correção de anti-patterns como:

- God Class / God Method
- Credenciais hardcoded
- SQL injection por concatenação
- Lógica de negócio em rotas/controller
- Endpoint administrativo inseguro
- Senhas com hash fraco
- Exposição de dados sensíveis em JSON
- Queries N+1 e duplicação de lógica
- Tratamento de erro inconsistente
- Uso excessivo de strings mágicas e logs sem estrutura

### Como a skill foi feita para ser agnóstica de tecnologia

- A análise começa com detecção de stack e arquitetura, sem depender de uma linguagem específica.
- O playbook de refatoração usa princípios genéricos de separação de responsabilidades, em vez de depender de um framework único.
- Para Python/Flask, a camada foi traduzida para modules de config, controllers e services.
- Para Node.js/Express, a mesma ideia foi aplicada com routes, controllers, services e config.
- A validação final é baseada em boot da aplicação e checagem de endpoints básicos, independentemente da tecnologia.

### Desafios encontrados

- A versão do Gemini CLI disponível no ambiente não aceitou o parâmetro de skill diretamente, então foi necessário criar um wrapper para executar o conteúdo do SKILL como prompt.
- Os projetos tinham níveis diferentes de organização, o que exigiu uma abordagem adaptável.
- Algumas aplicações já estavam rodando em portas padrão, então a validação precisou usar portas alternativas para evitar conflitos.

## C) Resultados

### Resumo dos relatórios de auditoria

Os relatórios foram gerados em:

- [reports/audit-project-1.md](reports/audit-project-1.md)
- [reports/audit-project-2.md](reports/audit-project-2.md)
- [reports/audit-project-3.md](reports/audit-project-3.md)

Resumo geral:

| Projeto | Severidade principal | Resultado estrutural esperado |
| --- | --- | --- |
| code-smells-project | CRITICAL/HIGH | Separação entre config, services e controllers; remoção de rotas inseguras |
| ecommerce-api-legacy | CRITICAL/HIGH | Camada de checkout isolada e configuração externa |
| task-manager-api | HIGH/MEDIUM | Menor acoplamento entre rotas e regras de negócio |

### Comparação antes/depois

- Antes: código monolítico, regras espalhadas por roteamento e acesso a banco.
- Depois: estrutura mais modular, com configuração centralizada, serviços para negócio e rotas mais enxutas.
- Antes: endpoints e lógica sensíveis misturados.
- Depois: endpoints preservados, com camada de serviço e tratamento mais claro de erros.

### Checklist de validação

- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Domínio da aplicação descrito corretamente
- [x] Número de arquivos analisados compatível com a realidade
- [x] Relatório segue o template definido
- [x] Findings ordenados por severidade
- [x] Mínimo de 5 findings por projeto identificado
- [x] Skill pausou antes da refatoração para revisão
- [x] Aplicações iniciaram e responderam a endpoints básicos

### Logs e validações executadas

#### 1. Python/Flask — code-smells-project

```bash
curl http://127.0.0.1:5000/health
{"ambiente":"producao","counts":{"pedidos":0,"produtos":10,"usuarios":3},"database":"connected","status":"ok"}
```

#### 2. Python/Flask — task-manager-api

```bash
curl http://127.0.0.1:5001/health
{"status":"ok","timestamp":"2026-06-28 18:13:25.766048"}
```

#### 3. Node.js/Express — ecommerce-api-legacy

```bash
curl -X POST http://127.0.0.1:3101/api/checkout -H 'Content-Type: application/json' -d '{"usr":"Ana","eml":"ana@email.com","pwd":"123456","c_id":2,"card":"4111111111111111"}'
{"msg":"Sucesso"}
```

> Como as aplicações são APIs, os resultados foram registrados como respostas HTTP e logs de execução, em vez de screenshots tradicionais.

## D) Como Executar

### Pré-requisitos

- Python 3.10+ com pip
- Node.js 20+ com npm
- Git para versionamento

### 1. Executar a skill no repositório inteiro

```bash
cd /home/carlos/mba/mba-ia-refactor-projects-skill
./.gemini/run-refactor-arch.sh
```

### 2. Executar a skill em cada projeto

#### code-smells-project

```bash
cd code-smells-project
../.gemini/run-refactor-arch.sh
```

#### ecommerce-api-legacy

```bash
cd ecommerce-api-legacy
../.gemini/run-refactor-arch.sh
```

#### task-manager-api

```bash
cd task-manager-api
../.gemini/run-refactor-arch.sh
```

### 3. Validar se a refatoração funcionou

#### Flask — loja

```bash
curl http://127.0.0.1:5000/health
```

#### Flask — task manager

```bash
curl http://127.0.0.1:5001/health
```

#### Express — checkout

```bash
PORT=3101 node src/app.js
curl -X POST http://127.0.0.1:3101/api/checkout -H 'Content-Type: application/json' -d '{"usr":"Ana","eml":"ana@email.com","pwd":"123456","c_id":2,"card":"4111111111111111"}'
```

### 4. Estrutura esperada após a refatoração

- [SKILL.md](.gemini/skills/refactor-arch/SKILL.md) com as instruções da skill
- [reports](reports) com os relatórios de auditoria
- pastas de config, controllers/services e rotas separadas por projeto

Se quiser, o próximo passo pode ser transformar esse README em uma versão ainda mais formal, com seção de arquitetura final e decisões de implementação por projeto.
