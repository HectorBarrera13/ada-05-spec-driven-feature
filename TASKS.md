# Tasks

## T-01 Project setup [COMPLETED]

- Goal: Configure project structure, package configuration (`pyproject.toml`), directory layout, sample data file, and base test harness.
- Files: `pyproject.toml`, `src/customer_search/__init__.py`, `tests/__init__.py`, `data/customers.json`
- Acceptance: Package `customer_search` is importable, initial data fixture exists, and pytest executes successfully.
- Verification: Run `pytest` to confirm environment and harness readiness.

## T-02 Domain model [COMPLETED]

- Goal: Implement the `Customer` entity and `SearchResult` value object with strong typing, immutability, and serialization.
- Files: `src/customer_search/models.py`, `tests/test_models.py`
- Acceptance: `Customer` model holds id, name, email, phone, and is_active flag. `SearchResult` encapsulates matching items, total count, query, and elapsed time.
- Verification: Run `pytest tests/test_models.py`.

## T-03 Search logic [COMPLETED]

- Goal: Implement `CustomerRepository` interface, in-memory repository with JSON loader, and `CustomerSearchService` with case-insensitive and diacritic-insensitive partial search.
- Files: `src/customer_search/repository.py`, `src/customer_search/service.py`, `tests/test_repository.py`, `tests/test_service.py`
- Acceptance: Search logic satisfies SR-01 to SR-06, supporting name, email, and unified search, sorting results alphabetically by customer name.
- Verification: Run `pytest tests/test_repository.py tests/test_service.py`.

## T-04 Validation and errors [COMPLETED]

- Goal: Implement custom exception hierarchy (`CustomerSearchValidationError`, `CustomerDataError`) and validation logic per VR-01 to VR-03.
- Files: `src/customer_search/exceptions.py`, `src/customer_search/validation.py`, `tests/test_validation.py`
- Acceptance: Validation rejects empty queries, whitespace-only queries, and queries shorter than 2 characters with informative error messages.
- Verification: Run `pytest tests/test_validation.py`.

## T-05 Tests & CLI [COMPLETED]

- Goal: Implement the CLI interface supporting `--query`, `--name`, `--email`, `--json`, and add integration tests and 10,000-record performance benchmark.
- Files: `src/customer_search/cli.py`, `tests/test_cli.py`, `tests/test_performance.py`
- Acceptance: CLI delivers tabular and JSON outputs with appropriate exit codes (0 for success, 2 for validation error), and benchmark executes in under 100ms.
- Verification: Run `pytest` across all tests and manually verify CLI invocations.

## T-06 Documentation

- Goal: Create comprehensive documentation, requirements traceability matrix, agent execution report, AI usage log, and project README with reflection answers.
- Files: `docs/traceability.md`, `results/agent-report.md`, `AI_USAGE_LOG.md`, `README.md`
- Acceptance: All documents required by ADA-05 are complete, coherent, and satisfy the Definition of Done.
- Verification: Verify all links, tables, test passes, and checklist items.
