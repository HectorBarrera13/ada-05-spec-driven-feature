"""Customer repository abstractions and implementations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol, Sequence

from customer_search.exceptions import CustomerDataError
from customer_search.models import Customer


class CustomerRepository(Protocol):
    """Protocol defining customer data access operations."""

    def get_all(self) -> list[Customer]:
        """Return all customer entities."""
        ...


class InMemoryCustomerRepository:
    """In-memory implementation of CustomerRepository."""

    def __init__(self, customers: Sequence[Customer] | None = None) -> None:
        self._customers: list[Customer] = list(customers or [])

    def get_all(self) -> list[Customer]:
        """Return a copy of all stored customers."""
        return list(self._customers)

    def add(self, customer: Customer) -> None:
        """Add a customer entity to repository."""
        self._customers.append(customer)

    @classmethod
    def from_json_file(cls, path: str | Path) -> InMemoryCustomerRepository:
        """Load customers from a JSON file path.

        Raises CustomerDataError if the file cannot be read or contains invalid data.
        """
        filepath = Path(path)
        if not filepath.exists() or not filepath.is_file():
            raise CustomerDataError(f"Customer data file not found at: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except json.JSONDecodeError as exc:
            raise CustomerDataError(f"Malformed JSON in customer data file: {exc}") from exc
        except OSError as exc:
            raise CustomerDataError(f"Error accessing customer data file: {exc}") from exc

        if not isinstance(raw_data, list):
            raise CustomerDataError("Invalid data format: Expected a JSON array of customer objects.")

        customers: list[Customer] = []
        for index, item in enumerate(raw_data):
            if not isinstance(item, dict):
                raise CustomerDataError(f"Invalid record at index {index}: Expected a JSON object.")
            try:
                customers.append(Customer.from_dict(item))
            except (KeyError, ValueError, TypeError) as exc:
                raise CustomerDataError(f"Invalid customer record at index {index}: {exc}") from exc

        return cls(customers)
