# Regras do Padrão MVC Alvo

## Objetivo do MVC

Separar responsabilidades para tornar o backend mais testável, manutenível e compreensível.

## Camadas

### Models
- Representam a estrutura de dados e persistência
- Devem conter a lógica de acesso ao banco ou abstrações de dados
- Não devem conhecer roteamento ou request/response

### Controllers / Services
- Orquestram a lógica de negócio entre models e views/routes
- Validam entrada e traduzem dados de/para as camadas de modelo
- Lidam com regras de domínio, cálculos, validação de transações e fluxos de negócio
- Não devem executar SQL direto no endpoint

### Views / Routes
- Definem endpoints HTTP e roteamento
- Recebem `request`, extraem parâmetros e chamam controllers/services
- Retornam respostas formatadas e tratam erros de alto nível
- Não devem conter lógica de negócio ou consultas diretas ao banco

## Configuração e Bootstrap
- `app.py` / `src/app.js` deve ser o ponto de entrada
- Configurações passadas por variáveis de ambiente ou módulo de config central
- Inicialização de banco, middlewares e rotas deve ser feita no composition root

## Tratamento de Erros
- Centralizar manejo de exceções em um middleware ou decorator
- Retornar objeto JSON padrão com `success`, `data`, `error`
- Evitar `print` ou logs de erro diretos dentro de funções de negócio

## Validação de Endpoints
- Rotas de saúde: `/health` ou `/status`
- Root endpoint `/` com metadata da aplicação
- Endpoints principais devem preservar nomes e métodos HTTP originais ou equivalentes
