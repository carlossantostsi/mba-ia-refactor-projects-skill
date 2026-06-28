# Audit Report - code-smells-project

Project: code-smells-project
Stack: Python + Flask
Files analyzed: app.py, controllers.py, models.py, database.py
Architecture: Monolithic legacy API with controllers and data access intermingled
Persistence: SQLite via sqlite3 direct queries

## Summary
- CRITICAL: 2
- HIGH: 3
- MEDIUM: 3
- LOW: 2

## Findings

### [CRITICAL] God Class / God Method
File: models.py / controllers.py
Description: A large portion of business logic, SQL access and response formatting is split across `controllers.py` and `models.py`. The application keeps routing, validation, persistence and business rules in only four files, making the architecture monolithic and hard to test.
Impact: High maintenance cost and strong coupling between HTTP layer and database layer.
Recommendation: Separate into models, services/controllers and routes/views.

### [CRITICAL] Hardcoded credentials and configuration inline
File: app.py:6
Description: `app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"` is stored directly in source code.
Impact: Secret leakage and environment-specific configuration cannot be changed safely.
Recommendation: Move config to a dedicated settings module or environment variables.

### [HIGH] SQL Injection risk from string concatenation
File: models.py (multiple functions: get_produto_por_id, get_usuario_por_id, criar_produto, atualizar_produto, deletar_produto, criar_pedido, get_pedidos_usuario, get_todos_pedidos)
Description: Several SQL queries are built by concatenating user-controlled values directly into the SQL string.
Impact: Attackers may execute arbitrary SQL or bypass validation.
Recommendation: Use parameterized queries or an ORM.

### [HIGH] Controllers contain business logic and side effects
File: controllers.py in functions like `criar_pedido`, `atualizar_produto`, `criar_usuario`
Description: HTTP route handlers perform validation, business rules, external side-effect logs, and error handling together.
Impact: Difficulty isolating business logic for unit tests, and inconsistent behavior across routes.
Recommendation: Move domain logic into service functions and keep routes thin.

### [HIGH] Dangerous admin query endpoint
File: app.py:60-82
Description: `/admin/query` executes arbitrary SQL from request body without authorization.
Impact: Critical security vulnerability and data corruption risk.
Recommendation: Remove this endpoint or restrict it heavily with parameterized queries and authentication.

### [MEDIUM] Duplicate row-to-dict mapping and repeated transformations
File: models.py multiple functions
Description: The same row conversion logic appears in several functions, violating DRY.
Impact: Higher chance of inconsistent output and harder refactoring.
Recommendation: Extract shared mappers/helpers.

### [MEDIUM] Inconsistent error handling and response format
File: controllers.py and app.py
Description: Some handlers log to console, others return raw exceptions or different JSON shapes.
Impact: Client responses are not normalized and debugging is more difficult.
Recommendation: Centralize error handling and standardize JSON responses.

### [MEDIUM] Unauthorized / admin routes mixed with public API
File: app.py:48-82
Description: `/admin/reset-db` and `/admin/query` exist alongside public routes with no authentication protective layer.
Impact: Insecure management surfaces exposed in production.
Recommendation: Move admin behavior to a dedicated module and secure it.

### [LOW] Magic strings and hardcoded status values
File: models.py and controllers.py
Description: Order statuses like `'pendente'`, `'aprovado'`, `'enviado'`, `'entregue'`, `'cancelado'` appear as literals.
Impact: Higher risk of typos and inconsistent business logic.
Recommendation: Define constants or enums.

### [LOW] Logging with print statements
File: controllers.py
Description: Uses `print()` for important workflow messages such as order creation and login.
Impact: Poor observability and no structure for logs in production.
Recommendation: Switch to a logging module and remove prints from business logic.

## Recommendations
- Refactor into MVC: separate route definitions, controllers/services and data access layers.
- Extract configuration to `config/settings.py` and use environment variables.
- Replace raw SQL concatenation with parameterized queries.
- Remove or secure the admin query endpoint.
- Introduce a centralized error handler and response schema.

## Validation Checklist
- [ ] Project boots successfully
- [ ] Main API endpoints still respond
- [ ] Configuration extracted
- [ ] MVC structure created
- [ ] No critical anti-patterns remaining
