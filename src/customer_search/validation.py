"""Validation rules and logic for Customer Search."""

from __future__ import annotations

from customer_search.exceptions import CustomerSearchValidationError


def validate_search_term(term: str | None, field_name: str = "query") -> str:
    """Validate a search term against VR-01, VR-02, and VR-03 rules.

    - VR-01: Must not be None or empty.
    - VR-02: Must not consist solely of whitespace.
    - VR-03: Must contain at least 2 characters after stripping whitespace.
    """
    if term is None or len(term) == 0:
        raise CustomerSearchValidationError(f"Search {field_name} must not be empty.")

    trimmed = term.strip()
    if not trimmed:
        raise CustomerSearchValidationError(
            f"Search {field_name} must not consist solely of whitespace."
        )

    if len(trimmed) < 2:
        raise CustomerSearchValidationError(
            f"Search {field_name} '{trimmed}' is too short. Minimum query length is 2 characters."
        )

    return trimmed


def validate_search_params(
    query: str | None = None,
    name: str | None = None,
    email: str | None = None,
) -> tuple[str | None, str | None, str | None]:
    """Validate that at least one search parameter is provided and all provided parameters are valid."""
    if query is None and name is None and email is None:
        raise CustomerSearchValidationError(
            "At least one search parameter ('query', 'name', or 'email') must be provided."
        )

    val_query = validate_search_term(query, "query") if query is not None else None
    val_name = validate_search_term(name, "name") if name is not None else None
    val_email = validate_search_term(email, "email") if email is not None else None

    return val_query, val_name, val_email
