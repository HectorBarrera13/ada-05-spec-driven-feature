# Requirements — Customer Search

## User Story

As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements

FR-01: The system shall allow searching customers by name (first name, last name, or combined full name) using case-insensitive partial and exact matching.
FR-02: The system shall allow searching customers by email address using case-insensitive partial and exact matching.
FR-03: The system shall support a unified search query that matches against both name and email fields simultaneously, as well as field-specific filtering by name or email.
FR-04: The system shall validate search queries, rejecting queries that are empty or consist solely of whitespace, and queries shorter than 2 characters, returning clear validation feedback.
FR-05: The system shall gracefully handle empty search results when no customers match the criteria, returning an empty list and a descriptive user message without raising unhandled errors.
FR-06: The system shall return customer search results containing customer ID, full name, email, phone number, and active status, ordered alphabetically by customer name.

## Non-Functional Requirements

NFR-01: Performance — Search execution time must be under 100 milliseconds for an in-memory dataset of up to 10,000 customer records.
NFR-02: Usability and CLI Interface — The system shall provide an intuitive CLI interface with informative help text (`--help`), standard exit codes (0 for success, non-zero for validation/runtime errors), and optional formatted JSON output (`--json`).
NFR-03: Maintainability and Testability — The implementation shall rely strictly on the Python standard library for runtime execution (zero external runtime dependencies) and maintain >90% automated test coverage runnable via `pytest`.

## Open Questions

Q-01: How should accented or special characters be handled during searches (e.g., "José" vs "Jose")?
Answer: Search queries and customer attributes shall undergo Unicode normalization (NFKD / diacritic removal during comparison) so that searches match regardless of accent marks.
Q-02: What format should seed data take for local CLI usage and testing?
Answer: Seed data can be provided via a local JSON file (`data/customers.json`) or generated programmatically via an in-memory fixture repository.

## Constraints / Assumptions

C-01: Standalone local execution without external databases or paid APIs (Python 3.11+ standard library + pytest for testing).
A-01: Customer IDs and email addresses in the active customer repository are assumed to be unique identifiers.
