# Catálogo de Anti-Patterns

## 1. God Class / God Method
- Severidade: CRITICAL
- Sinais: arquivo único ou método gigante que contém roteamento, validação, lógica de negócio e acesso a dados.
- Exemplo: `models.py` com consultas SQL diretas e funções de CRUD + lógica de pedido.
- Recomendação: extrair em `models`, `controllers` e possivelmente `services`.

## 2. Hardcoded Credentials / Config Inline
- Severidade: CRITICAL
- Sinais: `SECRET_KEY = "..."`, `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///...'`, strings de senha ou porta em código.
- Recomendação: mover para `config` ou variáveis de ambiente.

## 3. SQL Injection / Queries concatenadas
- Severidade: HIGH
- Sinais: concatenação de strings em SQL, `"SELECT ... WHERE id = " + id`, `cursor.execute(query_string)` com variáveis interpoladas diretamente.
- Recomendação: usar parâmetros seguros ou ORM.

## 4. Controllers com lógica de negócio pesada
- Severidade: HIGH
- Sinais: endpoints que calculam totais, validam estoque, montam objetos complexos ou executam várias queries.
- Recomendação: mover a lógica para `services` ou `models`.

## 5. API Deprecated / Uso de API obsoleta
- Severidade: MEDIUM
- Sinais: `express.Router()` sem `express.json()` em versões recentes, `body-parser` em vez de `express.json()`, `flask.ext` ou `Flask` APIs antigas.
- Recomendação: atualizar para a API atual do framework.

## 6. Seletor de rota / quebra de REST
- Severidade: MEDIUM
- Sinais: endpoint `/admin/query`, uso de verbs em nome de rota `/buscar_produto`, GET com body, múltiplas responsabilidades por rota.
- Recomendação: refatorar para rotas RESTful e segregação de endpoints.

## 7. Duplicação de código / DRY violado
- Severidade: MEDIUM
- Sinais: blocos muito semelhantes para transformar rows em dict, validação duplicada em várias rotas, queries repetidas.
- Recomendação: criar helpers, mapeadores e funções de reuso.

## 8. Error handling inconstante
- Severidade: LOW
- Sinais: respostas HTTP variadas `return {...}, 200`, `return jsonify({'erro': str(e)}), 500`, prints no console, mensagens não normalizadas.
- Recomendação: criar middlewares ou wrappers de error handling.

## 9. Magic numbers e strings
- Severidade: LOW
- Sinais: uso de `5000`, `'pendente'`, `'aprovado'`, `1`, `0` sem constante.
- Recomendação: extrair constantes ou enumerações.

## 10. Arquitetura sem configuração centralizada
- Severidade: LOW
- Sinais: config espalhada em `app.py`, `database.py`, `src/app.js`, `app.py`.
- Recomendação: criar `config/settings.py` ou `config/index.js`.
