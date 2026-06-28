# Audit Report - ecommerce-api-legacy

Project: ecommerce-api-legacy
Stack: Node.js + Express
Files analyzed: src/app.js, src/AppManager.js, src/utils.js
Architecture: Minimal Express app with business logic embedded in route setup
Persistence: SQLite in-memory database via sqlite3 direct queries

## Summary
- CRITICAL: 1
- HIGH: 3
- MEDIUM: 3
- LOW: 2

## Findings

### [CRITICAL] Hardcoded production secrets in source code
File: src/utils.js:4-6
Description: The application stores sensitive values such as `dbPass`, `paymentGatewayKey` and `smtpUser` directly in the codebase.
Impact: High risk of credential leakage and impossible configuration separation between environments.
Recommendation: Move all secrets to environment variables and use a config module.

### [HIGH] God Method in route definition
File: src/AppManager.js, `app.post('/api/checkout', ...)`
Description: The checkout route contains validation, payment processing, user creation, enrollment, auditing and response handling in one callback.
Impact: Hard to maintain, test or reuse, and mixes routing with domain logic.
Recommendation: Extract logic to controllers/services and keep route handler thin.

### [HIGH] Insecure user creation / password hashing
File: src/AppManager.js: `badCrypto(pwd || "123456")`
Description: The `badCrypto` function uses repeated base64 substrings instead of a secure hash algorithm.
Impact: Password security is weak and user accounts are vulnerable.
Recommendation: Replace with a standard hash library like bcrypt or argon2.

### [HIGH] Data consistency issues and orphaned records
File: src/AppManager.js, `/api/users/:id` delete endpoint
Description: Deleting a user does not cascade or clean up related enrollments and payments, leaving stale data.
Impact: Database integrity issues and inaccurate reporting.
Recommendation: Add proper referential integrity or cleanup logic.

### [MEDIUM] Deprecated or unnecessary middleware patterns
File: src/app.js
Description: The app uses `express.json()` correctly, but the code structure still follows an old-style manager object with route logic embedded.
Impact: The architecture is not modern and duplicates responsibilities.
Recommendation: Transition to `routes/`, `controllers/`, `services/` modules.

### [MEDIUM] Unsafe use of request body field names
File: src/AppManager.js, `/api/checkout`
Description: The route expects unconventional keys like `usr`, `eml`, `pwd`, `c_id`, `card` with no schema validation.
Impact: Higher chance of malformed requests and unclear API contract.
Recommendation: Use clear parameter names and validate request payloads.

### [MEDIUM] Multiple nested callbacks in route logic
File: src/AppManager.js, `/api/checkout`
Description: The checkout logic is deeply nested with sequential DB operations.
Impact: Error handling becomes fragile and the code is harder to refactor.
Recommendation: Flatten the flow using services, promises, or async/await.

### [LOW] Magic numbers and hardcoded statuses
File: src/AppManager.js
Description: Values like `'PAID'`, `'DENIED'`, `1`, `'123'` and the card check `cc.startsWith("4")` are hardcoded.
Impact: Behavior is opaque and brittle.
Recommendation: Use constants and feature flags.

### [LOW] Logging to console without structured output
File: src/AppManager.js, src/utils.js
Description: The app uses `console.log` for audit and flow logs.
Impact: No structured log format and no separation between debug and production output.
Recommendation: Introduce a logging abstraction.

## Recommendations
- Refactor to MVC with explicit `routes/`, `controllers/`, `services/`, and `config/`.
- Move config and secrets to environment variables.
- Replace weak hashing with a secure password algorithm.
- Simplify the checkout flow and make it testable.
- Add data cleanup / cascade delete for users.

## Validation Checklist
- [ ] App starts successfully
- [ ] Checkout endpoint still responds
- [ ] Config extracted
- [ ] MVC structure created
- [ ] No critical anti-patterns remaining
