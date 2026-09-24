"""Customer search business logic and service layer."""

from __future__ import annotations

import time
import unicodedata
from typing import Sequence

from customer_search.exceptions import CustomerSearchValidationError
from customer_search.models import Customer, SearchResult
from customer_search.repository import CustomerRepository


def normalize_text(text: str) -> str:
    """Normalize text using Unicode NFKD, stripping diacritics and converting to lowercase."""
    if not text:
        return ""
    # Normalize Unicode composition to decompose accents
    decomposed = unicodedata.normalize("NFKD", text)
    # Strip diacritical marks (category 'Mn')
    stripped = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return stripped.strip().casefold()


def validate_search_term(term: str | None, field_name: str = "query") -> str:
    """Validate a search term against VR-01, VR-02, and VR-03 rules."""
    if term is None or len(term) == 0:
        raise CustomerSearchValidationError(f"Search {field_name} must not be empty.")

    trimmed = term.strip()
    if not trimmed:
        raise CustomerSearchValidationError(f"Search {field_name} must not consist solely of whitespace.")

    if len(trimmed) < 2:
        raise CustomerSearchValidationError(
            f"Search {field_name} '{trimmed}' is too short. Minimum query length is 2 characters."
        )

    return trimmed


class CustomerSearchService:
    """Coordinates search execution across customer records."""

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def search(
        self,
        query: str | None = None,
        name: str | None = None,
        email: str | None = None,
    ) -> SearchResult:
        """Search customers by unified query, name, or email.

        Satisfies FR-01, FR-02, FR-03, FR-04, FR-05, FR-06.
        """
        start_time = time.perf_counter()

        # Check that at least one search parameter was provided
        if query is None and name is None and email is None:
            raise CustomerSearchValidationError(
                "At least one search parameter ('query', 'name', or 'email') must be provided."
            )

        validated_query = validate_search_term(query, "query") if query is not None else None
        validated_name = validate_search_term(name, "name") if name is not None else None
        validated_email = validate_search_term(email, "email") if email is not None else None

        norm_query = normalize_text(validated_query) if validated_query else None
        norm_name = normalize_text(validated_name) if validated_name else None
        norm_email = normalize_text(validated_email) if validated_email else None

        all_customers = self._repository.get_all()
        matched: list[Customer] = []

        for customer in all_customers:
            cust_name_norm = normalize_text(customer.name)
            cust_email_norm = normalize_text(customer.email)

            is_match = False

            # Unified query (FR-03, SR-04): matches name OR email
            if norm_query:
                if norm_query in cust_name_norm or norm_query in cust_email_norm:
                    is_match = True

            # Specific name search (FR-01, SR-05)
            if norm_name:
                if norm_name in cust_name_norm:
                    is_match = True

            # Specific email search (FR-02, SR-05)
            if norm_email:
                if norm_email in cust_email_norm:
                    is_match = True

            if is_match:
                matched.append(customer)

        # Deduplicate while preserving order if multiple criteria matched
        seen_ids: set[str] = set()
        unique_matches: list[Customer] = []
        for customer in matched:
            if customer.id not in seen_ids:
                seen_ids.add(customer.id)
                unique_matches.append(customer)

        # Ordering (SR-06, FR-06): alphabetically by customer name, secondary by id
        sorted_customers = sorted(
            unique_matches,
            key=lambda c: (c.name.casefold(), c.id),
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        used_query_repr = (
            f"query='{validated_query}'"
            if validated_query
            else f"name='{validated_name}'"
            if validated_name
            else f"email='{validated_email}'"
        )

        return SearchResult(
            customers=sorted_customers,
            total_count=len(sorted_customers),
            query=used_query_repr,
            execution_time_ms=elapsed_ms,
        )
