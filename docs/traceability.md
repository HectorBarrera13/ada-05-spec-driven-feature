# Requirements Traceability Matrix

This matrix establishes end-to-end traceability connecting each requirement defined in [REQUIREMENTS.md](../REQUIREMENTS.md) to its verifiable specification in [SPEC.md](../SPEC.md), task breakdown in [TASKS.md](../TASKS.md), source code implementation, and automated test cases.

| Requirement | SPEC / AC | Task | Files | Test | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** | AC-01, SR-01, SR-02, SR-03, SR-05 | T-03 | `src/customer_search/service.py` | `tests/test_service.py::test_search_by_name_exact`, `test_search_by_name_partial_case_insensitive`, `test_search_by_name_diacritics` | Verified | Case-insensitive & diacritic-insensitive search by customer name |
| **FR-02** | AC-02, SR-01, SR-03, SR-05 | T-03 | `src/customer_search/service.py` | `tests/test_service.py::test_search_by_email_partial` | Verified | Case-insensitive search by customer email |
| **FR-03** | AC-03, SR-04 | T-03 | `src/customer_search/service.py` | `tests/test_service.py::test_unified_query_searches_name_and_email`, `test_unified_query_deduplicates_matches` | Verified | Matches against name OR email without duplicating records |
| **FR-04** | AC-04, VR-01, VR-02, VR-03 | T-04 | `src/customer_search/validation.py` | `tests/test_validation.py::test_validate_search_term_empty`, `test_validate_search_term_whitespace`, `test_validate_search_term_too_short` | Verified | Rejects empty, whitespace-only, and <2 char queries with validation error |
| **FR-05** | AC-05, EH-03 | T-03, T-05 | `src/customer_search/service.py`, `src/customer_search/cli.py` | `tests/test_service.py::test_search_empty_results`, `tests/test_cli.py::test_cli_zero_matches` | Verified | Gracefully returns empty list and user message, exit code 0 |
| **FR-06** | AC-06, SR-06 | T-02, T-03 | `src/customer_search/models.py`, `src/customer_search/service.py` | `tests/test_models.py::test_customer_creation`, `tests/test_service.py::test_search_alphabetical_ordering` | Verified | Returns full customer record payload, sorted alphabetically by name |
| **NFR-01** | AC-07 | T-05 | `src/customer_search/service.py` | `tests/test_performance.py::test_performance_10k_records` | Verified | Benchmarked < 100ms on 10,000 in-memory records (~15-25ms measured) |
| **NFR-02** | AC-08, EH-01, EH-02 | T-05 | `src/customer_search/cli.py` | `tests/test_cli.py::test_cli_positional_search`, `test_cli_json_output`, `test_cli_validation_error_short`, `test_cli_data_file_missing` | Verified | Clear CLI flags (`--query`, `--name`, `--email`, `--data`, `--json`), standard exit codes (0, 1, 2) |
| **NFR-03** | AC-09 | T-01, T-05 | `pyproject.toml`, all source files | All 36 automated pytest tests | Verified | 0 runtime dependencies (pure standard library), 100% test pass rate |
