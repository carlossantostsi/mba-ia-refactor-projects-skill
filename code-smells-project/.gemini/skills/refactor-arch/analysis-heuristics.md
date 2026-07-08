# Análise de Projeto — Heurísticas

## Detecção de linguagem e framework

### Python
- Presença de arquivos `.py`
- Importações como `flask`, `flask_cors`, `sqlalchemy`, `sqlite3`
- Uso de `app = Flask(__name__)`
- Uso de `from flask import`

### Node.js
- Presença de `package.json`
- Arquivos `.js` ou `.mjs`
- Importações ou requires como `express`, `body-parser`, `mongoose`, `sequelize`
- Uso de `const app = express()` ou `app.listen(...)`

## Identificação de persistência / banco de dados

- `sqlite:///`, `sqlite3`, `pymysql`, `psycopg2`, `sqlalchemy` → banco relacional
- `mysql`, `postgres`, `mssql`, `pg`, `mysql2`, `sqlite3` → SQL
- `mongodb`, `mongoose` → banco NoSQL
- Executar query string direta no código (`cursor.execute("SELECT..."`) ou `db.query(...)`)
- Presença de `models/`, `entities/`, `schemas/`

## Mapeamento de arquitetura

### Monolítica
- Tudo está em 1 ou 2 arquivos principais
- Lógica de negócio, persistência e roteamento misturados no mesmo arquivo
- Configuração e segredos inline

### Parcialmente modularizada
- Existem `models/`, `routes/`, `services/` ou `controllers/` mas ainda há mistura de responsabilidades
- Há `utils/` e `database.py`, mas controllers ainda fazem consultas diretas ou validação de negócio

### Organizada em camadas
- Separação clara entre: models, controllers/services, routes/views, config
- Tratamento de erros centralizado
- Use de funções ou classes de serviço para lógica de negócio

## Sinais de domínio e contexto

- Rota ou função que menciona `produto`, `usuario`, `pedido`, `task`, `login`, `checkout`
- Arquivo `README.md` com descrições de API
- Uso de `@app.route` ou `router.get/post/put/delete`

## Saída de análise esperada

- Language: Python ou Node.js
- Framework: Flask, Express, FastAPI, etc.
- Persistence: SQLite / SQL / NoSQL / Arquivo
- Architecture: Monolithic / Partially Modular / Layered
- Domains: e-commerce, tasks, LMS, Auth, Reports
- Files analyzed: lista de arquivos relevantes
