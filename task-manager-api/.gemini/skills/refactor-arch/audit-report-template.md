# Template de Relatório de Auditoria

## Audit Report

Project: {project_name}
Stack: {language} + {framework}
Files analyzed: {files_count}
Architecture: {architecture}
Persistence: {persistence}

## Summary
- CRITICAL: {critical_count}
- HIGH: {high_count}
- MEDIUM: {medium_count}
- LOW: {low_count}

## Findings

### [{severity}] {title}
File: {file_path}:{line}
Description: {description}
Impact: {impact}
Recommendation: {recommendation}

---

## Recommendations
- Refatorar para MVC com separação de responsabilidades
- Remover hardcoded credentials e mover para config
- Normalizar tratamento de erros e respostas JSON
- Atualizar APIs deprecated identificadas

## Validation Checklist
- [ ] Project boots successfully
- [ ] Endpoints respond correctly
- [ ] Configuration extracted
- [ ] MVC structure created
- [ ] No critical anti-patterns remaining
