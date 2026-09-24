# Agent Report

## Agent / Version

- **Agent**: Antigravity CLI (agy) / Gemini 3.8 Flash (High)
- **Environment**: macOS, Python 3.14.3, pytest 9.1.1, Git

## Initial Context

- Starting project from scratch without base repository.
- Baseline requirements and specification defined in `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, and `AGENTS.md`.
- Baseline git commit initialized prior to feature implementation: `"spec: define customer search feature"`.

## Task Sequence

### T-01 Project setup
- **What the agent did**: Configured `pyproject.toml` packaging, created `src/customer_search/__init__.py`, `tests/__init__.py`, seed dataset `data/customers.json`, and smoke test `tests/test_setup.py`. Configured pytest options to disable cacheprovider warnings in sandboxed environments.
- **Human review**: Validated project structure, package imports, and test harness execution.
- **Tests**: `pytest tests/test_setup.py` PASSED (1/1).

### T-02 Domain model
- **What the agent did**: Implemented `Customer` frozen dataclass entity and `SearchResult` value object in `src/customer_search/models.py`. Added unit tests in `tests/test_models.py` covering field validation, immutability, serialization (`to_dict`/`from_dict`), and timing.
- **Human review**: Reviewed model immutability and fixed a minor floating point assertion edge case involving banker's rounding (`1.2345` -> `1.25`).
- **Tests**: `pytest tests/test_models.py` PASSED (5/5).

### T-03 Search logic
- **What the agent did**: Defined `CustomerRepository` Protocol and `InMemoryCustomerRepository` in `src/customer_search/repository.py` with JSON file loading capability. Implemented `CustomerSearchService` in `src/customer_search/service.py` featuring Unicode NFKD diacritic normalization, case-insensitive substring search across name and email, match deduplication, and alphabetical ordering (SR-01 to SR-06).
- **Human review**: Validated search matching rules, accented character behavior ("José" == "jose"), and alphabetical sorting.
- **Tests**: `pytest tests/test_repository.py tests/test_service.py` PASSED (14/14).

### T-04 Validation and errors
- **What the agent did**: Created `src/customer_search/exceptions.py` with domain exceptions (`CustomerSearchValidationError`, `CustomerDataError`). Extracted and modularized validation logic into `src/customer_search/validation.py` enforcing VR-01 (presence), VR-02 (non-whitespace), and VR-03 (minimum 2 characters). Added comprehensive tests in `tests/test_validation.py`.
- **Human review**: Verified clear, actionable error messages on query validation failures.
- **Tests**: `pytest tests/test_validation.py` PASSED (7/7).

### T-05 Tests & CLI
- **What the agent did**: Implemented user-friendly CLI in `src/customer_search/cli.py` with positional query support, `-q/--query`, `-n/--name`, `-e/--email`, `-d/--data`, and `--json`. Handled standard exit codes (0 for success, 2 for validation errors, 1 for runtime errors). Implemented end-to-end integration tests in `tests/test_cli.py` and benchmark test in `tests/test_performance.py` verifying search on 10,000 records.
- **Human review**: Verified CLI tabular rendering, `--json` formatting, and confirmed 10k-record benchmark ran in ~15-25ms (<100ms threshold).
- **Tests**: `pytest tests/test_cli.py tests/test_performance.py` PASSED (9/9). Full suite PASSED (36/36).

### T-06 Documentation
- **What the agent did**: Generated `docs/traceability.md`, `results/agent-report.md`, `AI_USAGE_LOG.md`, and comprehensive `README.md` addressing installation, usage, architecture, and the 12 reflection questions from Section 18. Marked all tasks completed in `TASKS.md`.
- **Human review**: Verified consistency across all artifacts, requirements mapping, and definition of done.
- **Tests**: Clean pytest run on entire suite (36/36 passed).

## Problems Encountered

1. **Pytest Cache Permission in Sandbox**: Pytest emitted a warning trying to create `.pytest_cache` in the sandboxed directory. Resolved cleanly by setting `addopts = "-p no:cacheprovider"` in `pyproject.toml`.
2. **Banker's Rounding in Floating-Point Test**: Testing `round(1.2345, 3)` produced `1.234` instead of `1.235` due to Python's round-half-to-even behavior. Resolved by asserting on an exact floating point number (`1.25`) in `tests/test_models.py`.
3. **Single-Character Test Query**: An initial alphabetical test used query `"."`, which triggered the validation rule VR-03 (<2 characters). This proved that validation rules were actively guarding query execution; the test was updated to use a valid multi-character substring `"es"`.

## Human Interventions

- Approved requirement scope and non-functional requirements (performance benchmark, zero external runtime dependencies).
- Confirmed Unicode NFKD normalization strategy to handle diacritics and accents.
- Directed separation of query validation into its own module (`validation.py`).

## Requirement / Specification Changes

No requirements or specifications were altered to force tests to pass. All initial specifications remained intact throughout the implementation cycle.

## Final Verification

- Total automated tests: **36 tests passed** in **0.36 seconds**.
- Performance benchmark: 10,000 customer records searched in **~15-25 ms** (well below the 100ms budget of NFR-01).
- CLI exit codes verified:
  - Valid query: `0`
  - Zero matches: `0`
  - Validation error: `2`
  - Data / file error: `1`

## Lessons Learned

- **Spec-driven development prevents rework**: Having strict, immutable requirements (FR-01 to FR-06) and verifiable acceptance criteria (AC-01 to AC-09) before coding ensured the coding agent implemented exactly what was required without inventing unwanted features or hallucinating business rules.
- **Separation of REQUIREMENTS.md and SPEC.md**: Keeping the user requirements separate from technical specifications allows product stakeholders to understand what the feature does, while providing developers and agents with unambiguous contracts and verification criteria.
- **Strict AGENTS.md rules keep agents on track**: Guardrails such as "do not invent business requirements" and "do not modify specs to make tests pass" prevented shortcuts and ensured clean, disciplined software engineering.
