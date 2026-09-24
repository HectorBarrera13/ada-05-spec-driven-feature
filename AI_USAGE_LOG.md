# AI Usage Log — ADA-05 Spec-Driven Feature

This document records the key interactions, AI proposals, human engineering decisions, and product impacts across the spec-driven development lifecycle of ADA-05.

---

### Entry 1: Requirements & Specification Definition (Fases 1 y 2)
- **Stage**: Requirements & Specification (`REQUIREMENTS.md`, `SPEC.md`)
- **Context / Prompt**:
  The developer asked to establish complete functional and non-functional requirements for the Customer Search feature, allowing flexibility in criteria while strictly honoring the template and rules from the ADA-05 specification.
- **AI Proposal**:
  The AI proposed a feature scope with 6 functional requirements (FR-01 to FR-06) covering case-insensitive partial search by name, email, unified query, validation rules (>= 2 chars), empty results handling, and alphabetical sorting. For non-functional requirements (NFR-01 to NFR-03), it proposed <100ms performance across 10k records, CLI usability with `--json` and standard exit codes, and zero third-party runtime dependencies.
- **Human Decision / Adjustment**:
  Accepted the requirement set. Clarified the handling of special characters (Q-01) by establishing explicit Unicode NFKD normalization so accents like "José" match "jose", and stipulated that seed data should default to a local JSON file (`data/customers.json`). Ensured that `SPEC.md` strictly referenced requirements by ID without duplicating their definitions.
- **Impact on Product**:
  Created well-defined, verifiable criteria and boundaries preventing scope creep before any code was written.

---

### Entry 2: Architectural Modeling and Layered Design (Fase 3)
- **Stage**: Architecture (`ARCHITECTURE.md`)
- **Context / Prompt**:
  Designing the components, responsibilities, data flow, and interfaces for the Customer Search CLI tool.
- **AI Proposal**:
  The AI suggested a clean layered architecture with a Domain Model (`Customer`, `SearchResult`), Repository Protocol (`CustomerRepository`), Service Layer (`CustomerSearchService`), and Presentation CLI (`cli.py`). It also evaluated whether to use an inverted index (or SQLite FTS) vs an in-memory linear scan.
- **Human Decision / Adjustment**:
  Opted for the in-memory linear scan with Unicode normalization. For datasets of up to 10,000 records, linear scanning executes in ~15ms, eliminating unnecessary dependency overhead and database synchronization bugs while keeping the project 100% compliant with standard library constraints (C-01).
- **Impact on Product**:
  Kept codebase lightweight, modular, testable with pure mocks/fixtures, and completely dependency-free.

---

### Entry 3: Domain Implementation & Validation Separation (Fases 4 y 7: T-02, T-03, T-04)
- **Stage**: Implementation & Refactoring (`src/customer_search/`)
- **Context / Prompt**:
  Implement the domain entity, repository, search service, and validation logic according to tasks T-02, T-03, and T-04.
- **AI Proposal**:
  Initially, the AI implemented validation logic directly inside `service.py`. When testing serialization in `test_models.py`, Python's `round(1.2345, 3)` produced `1.234` due to banker's rounding (round half to even).
- **Human Decision / Adjustment**:
  1. Decoupled validation into its own module (`src/customer_search/validation.py`) to adhere to the Single Responsibility Principle and allow independent unit testing of query boundary conditions (VR-01, VR-02, VR-03).
  2. Fixed floating-point test assertions to use stable non-ambiguous representations (`1.25`).
- **Impact on Product**:
  Cleaner separation of concerns, 100% test isolation for validation rules, and resilient test assertions.

---

### Entry 4: CLI Implementation, Performance Verification & Delivery (Fases 4, 7, 8, 9: T-05, T-06)
- **Stage**: Testing, CLI Presentation & Verification (`cli.py`, `test_cli.py`, `test_performance.py`)
- **Context / Prompt**:
  Implement the CLI interface, end-to-end integration tests, and automate verification of NFR-01 (10,000 records under 100ms).
- **AI Proposal**:
  The AI proposed adding positional argument support in addition to explicit `-q/--query`, `-n/--name`, and `-e/--email` flags, along with a benchmark test generating 10,000 synthetic records. It suggested standard POSIX exit codes: 0 for success/no matches, 2 for validation errors, and 1 for file/runtime errors.
- **Human Decision / Adjustment**:
  Accepted the CLI design and exit code specification. Verified that `pytest` executed all 36 tests cleanly and that the 10,000-record benchmark executed in ~15-25ms (well under the 100ms threshold).
- **Impact on Product**:
  Delivered a polished, user-friendly terminal experience with full tabular and JSON output options, verified by automated end-to-end and benchmark tests.
