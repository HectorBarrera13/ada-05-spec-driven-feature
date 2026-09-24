"""Domain models for Customer Search feature."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Customer:
    """Represents a customer domain entity."""

    id: str
    name: str
    email: str
    phone: str
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Customer id must be a non-empty string.")
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Customer name must be a non-empty string.")
        if not self.email or not isinstance(self.email, str):
            raise ValueError("Customer email must be a non-empty string.")

    def to_dict(self) -> dict[str, Any]:
        """Convert customer entity to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Customer:
        """Create Customer entity from dictionary."""
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            phone=str(data.get("phone", "")),
            is_active=bool(data.get("is_active", True)),
        )


@dataclass(frozen=True)
class SearchResult:
    """Represents the outcome of a customer search operation."""

    customers: list[Customer]
    total_count: int
    query: str
    execution_time_ms: float

    def to_dict(self) -> dict[str, Any]:
        """Convert search result to dictionary."""
        return {
            "customers": [c.to_dict() for c in self.customers],
            "total_count": self.total_count,
            "query": self.query,
            "execution_time_ms": round(self.execution_time_ms, 3),
        }
