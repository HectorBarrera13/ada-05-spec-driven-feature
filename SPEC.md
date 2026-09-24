# Customer Search Feature

## Goal

Provide a robust, fast, and user-friendly customer search component and CLI tool capable of finding customers by name or email with case-insensitive partial matching, input validation, and structured output formatting.

## Requirements Covered

- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- NFR-01
- NFR-02
- NFR-03

## Scope

- In-memory customer repository with optional JSON seed file loading.
- Core search service supporting case-insensitive and diacritic-insensitive partial matching.
- Search queries over name, email, or unified combined search.
- Query validation with explicit error diagnostics.
- Command-line interface (CLI) with human-readable table output, `--json` formatting, and standard exit codes.
- Automated test suite validating all functional and non-functional requirements.

## Out of Scope

- External SQL or NoSQL database integration.
- User authentication, role-based authorization, and session management.
- Customer record mutation (create, update, delete) operations.
- HTTP web server endpoints (CLI is the primary interface for ADA-05).

## Domain Model

### Customer Entity
- `id` (str): Unique customer identifier (e.g., "CUST-001").
- `name` (str): Full customer name (e.g., "Alice Smith").
- `email` (str): Contact email address (e.g., "alice@example.com").
- `phone` (str): Contact phone number (e.g., "+1-555-0101").
- `is_active` (bool): Account status indicator (default: True).

### SearchResult Value Object
- `customers` (list[Customer]): Ordered list of matching customer entities.
- `total_count` (int): Number of matched records.
- `query` (str): Search term used.
- `execution_time_ms` (float): Elapsed execution time in milliseconds.

## Search Rules

- SR-01 (Case Insensitivity): All query comparisons against customer fields are case-insensitive (using Unicode casefolding).
- SR-02 (Diacritic Normalization): Accented characters (e.g., "é", "ñ", "ü") are normalized to their base representation during search so that "jose" matches "José".
- SR-03 (Substring Matching): A record matches if the normalized search term is a contiguous substring of the target field.
- SR-04 (Unified Search): When general search query is provided, match occurs if the query matches `name` OR `email`.
- SR-05 (Field-Specific Search): When `--name` is specified, search only targets `name`. When `--email` is specified, search only targets `email`.
- SR-06 (Ordering): Resulting customer records are sorted alphabetically by `name` in ascending order. If names are identical, secondary sort is by `id`.

## Validation Rules

- VR-01 (Presence): Query strings must not be None or empty.
- VR-02 (Non-Whitespace): Query strings must not consist solely of whitespace characters.
- VR-03 (Minimum Length): Search queries must contain at least 2 characters after trimming leading/trailing whitespace.

## Error Handling

- EH-01: Validation errors raise `CustomerSearchValidationError`. In CLI, this prints an error message to stderr and exits with exit code 2.
- EH-02: Missing or corrupted data files raise `CustomerDataError`. In CLI, this prints an error to stderr and exits with exit code 1.
- EH-03: Zero matching records is not an error condition. The system returns an empty list, displays a clear message to the user, and exits with code 0.

## Acceptance Criteria

- AC-01 (Covering FR-01): Searching by name substring (e.g., "an") matches customers whose name contains "an" regardless of case or diacritics, sorted alphabetically.
- AC-02 (Covering FR-02): Searching by email substring (e.g., "corp") matches customers whose email contains "corp" regardless of case.
- AC-03 (Covering FR-03): A unified query returns customers matching name OR email without duplicated records in the result set.
- AC-04 (Covering FR-04): Passing an empty query, whitespace, or a query with fewer than 2 characters triggers validation failure with descriptive error text.
- AC-05 (Covering FR-05): When zero customers match, the search returns an empty collection and displays "No customers found matching '<query>'." with exit code 0.
- AC-06 (Covering FR-06): Search output contains customer id, name, email, phone, and is_active status, sorted alphabetically by name.
- AC-07 (Covering NFR-01): Search across 10,000 customer records in memory executes in under 100 milliseconds.
- AC-08 (Covering NFR-02): CLI tool provides `--help`, supports `--name`, `--email`, `--query`, `--json`, and adheres to exit codes (0 for success, 2 for validation error, 1 for runtime error).
- AC-09 (Covering NFR-03): Core logic has zero third-party runtime dependencies and automated test suite passes via `pytest`.

## Test Scenarios

- TS-01: Exact name match ("Jane Doe") returns the matching customer.
- TS-02: Partial name match ("jan") returns all matching records case-insensitively.
- TS-03: Diacritic name match ("jose" matches "José") returns matching customer.
- TS-04: Email substring match ("example.com") returns all customers with that email domain.
- TS-05: Validation failure on query shorter than 2 characters ("a") or blank spaces ("   ").
- TS-06: Zero matches query ("xyznonexistent") returns empty list and notification.
- TS-07: CLI invocation with `--json` outputs valid JSON array of customer objects.
- TS-08: CLI invocation with invalid arguments exits with code 2.
- TS-09: Benchmark test verifies that searching 10,000 records takes under 100 ms.

## Constraints

- Reliance solely on Python 3.11+ standard library for implementation (C-01).

## Open Questions

- N/A: All questions from REQUIREMENTS.md have been resolved and captured in rules SR-02 and repository design.
