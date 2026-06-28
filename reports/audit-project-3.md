# Audit Report - task-manager-api

Project: task-manager-api
Stack: Python + Flask + SQLAlchemy
Files analyzed: app.py, routes/task_routes.py, routes/user_routes.py, routes/report_routes.py, models/task.py, models/user.py, models/category.py, database.py
Architecture: Partially modular but still mixing business rules and response presentation in route handlers
Persistence: SQLite via SQLAlchemy ORM

## Summary
- CRITICAL: 0
- HIGH: 3
- MEDIUM: 4
- LOW: 3

## Findings

### [HIGH] Business logic in route handlers
File: routes/task_routes.py and routes/user_routes.py
Description: Routes perform validation, data transformation, password hashing, overdue calculation, and nested queries directly.
Impact: Harder to unit-test and violates single responsibility.
Recommendation: Move domain logic to service or model methods.

### [HIGH] Password hashing using MD5
File: models/user.py: `set_password`, `check_password`
Description: The application uses MD5 for password hashing.
Impact: MD5 is insecure for authentication and vulnerable to collision and brute-force attacks.
Recommendation: Use a salted secure hash such as bcrypt or argon2.

### [HIGH] Sensitive data returned in API responses
File: models/user.py: `to_dict()` returns `password`
Description: User responses expose hashed password values.
Impact: Exposure of authentication data to clients.
Recommendation: Remove password from serialized user output.

### [MEDIUM] Duplicate overdue calculation logic
File: routes/task_routes.py, routes/user_routes.py, models/task.py
Description: The same overdue logic is repeated in multiple places instead of a shared helper.
Impact: Increased maintenance burden and inconsistent behavior.
Recommendation: Centralize overdue logic in the model or service layer.

### [MEDIUM] Inefficient query usage and N+1 risk
File: routes/task_routes.py and routes/user_routes.py
Description: `Task.query.get()` and `User.query.get()` inside loops may generate extra queries.
Impact: Performance degradation as data volume grows.
Recommendation: Use joined loading or explicit query batches.

### [MEDIUM] Generic error handling
File: routes/task_routes.py, routes/user_routes.py, routes/report_routes.py
Description: Some routes catch all exceptions and return generic error messages while swallowing the real exception.
Impact: Hard to diagnose production errors and inconsistent response format.
Recommendation: Implement centralized error handling and consistent JSON error schemas.

### [MEDIUM] Inconsistent validation and response format
File: routes/task_routes.py, routes/user_routes.py
Description: Routes use multiple different response structures and status codes for similar validation errors.
Impact: Client integration becomes harder and API behavior is not standardized.
Recommendation: Standardize validation errors and success responses.

### [LOW] Magic strings in status and role fields
File: routes/task_routes.py, routes/user_routes.py
Description: Status values and role names are hardcoded in many places.
Impact: Typos and inconsistent domain rules.
Recommendation: Define constants or enumerations for statuses and roles.

### [LOW] Unused imports and broad exception catches
File: routes/task_routes.py, routes/report_routes.py
Description: Some route modules import `sys`, `json`, `os`, `time` without use and catch bare exceptions.
Impact: Code clarity issues and swallowed exceptions.
Recommendation: Remove unused imports and catch specific exception types.

### [LOW] Model serialization duplicates route logic
File: models/task.py, routes/task_routes.py
Description: The route builds dictionaries while models also provide `to_dict()`, causing duplication.
Impact: Higher risk of inconsistent output.
Recommendation: Use model serialization consistently.

## Recommendations
- Refactor to a clearer MVC structure with `services/` between `routes/` and `models/`.
- Replace MD5 password hashing and avoid leaking password fields in API output.
- Consolidate validation and overdue status logic.
- Add centralized error handling and response formatting.
- Keep endpoints intact while improving architecture.

## Validation Checklist
- [ ] App boots successfully
- [ ] Main task/user/report endpoints still respond
- [ ] Password storage hardened
- [ ] MVC structure improved
- [ ] No high anti-patterns remaining
