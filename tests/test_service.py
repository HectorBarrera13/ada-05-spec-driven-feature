"""Tests for customer search service logic."""

import pytest
from customer_search.exceptions import CustomerSearchValidationError
from customer_search.models import Customer
from customer_search.repository import InMemoryCustomerRepository
from customer_search.service import CustomerSearchService, normalize_text


@pytest.fixture
def service() -> CustomerSearchService:
    customers = [
        Customer(id="C1", name="Alice Johnson", email="alice.j@example.com", phone="111", is_active=True),
        Customer(id="C2", name="Bob Smith", email="bob.smith@acme.org", phone="222", is_active=True),
        Customer(id="C3", name="José García", email="jose.garcia@soluciones.mx", phone="333", is_active=True),
        Customer(id="C4", name="María Fernández", email="maria.f@empresa.es", phone="444", is_active=True),
        Customer(id="C5", name="Jane Doe", email="jane.doe@example.com", phone="555", is_active=True),
        Customer(id="C6", name="John Doe", email="john.doe@example.com", phone="666", is_active=False),
    ]
    repo = InMemoryCustomerRepository(customers)
    return CustomerSearchService(repo)


def test_normalize_text():
    assert normalize_text("  José García  ") == "jose garcia"
    assert normalize_text("MARÍA") == "maria"
    assert normalize_text("Café") == "cafe"


def test_search_by_name_exact(service: CustomerSearchService):
    result = service.search(name="Jane Doe")
    assert result.total_count == 1
    assert result.customers[0].name == "Jane Doe"


def test_search_by_name_partial_case_insensitive(service: CustomerSearchService):
    result = service.search(name="doe")
    assert result.total_count == 2
    # Alphabetical order: Jane Doe before John Doe
    assert [c.name for c in result.customers] == ["Jane Doe", "John Doe"]


def test_search_by_name_diacritics(service: CustomerSearchService):
    # Searching "jose" should match "José García"
    result = service.search(name="jose")
    assert result.total_count == 1
    assert result.customers[0].name == "José García"

    # Searching "garcia" without accent
    result2 = service.search(name="garcia")
    assert result2.total_count == 1
    assert result2.customers[0].name == "José García"


def test_search_by_email_partial(service: CustomerSearchService):
    result = service.search(email="acme.org")
    assert result.total_count == 1
    assert result.customers[0].name == "Bob Smith"


def test_unified_query_searches_name_and_email(service: CustomerSearchService):
    # "example.com" is in email of Alice, Jane, John
    result = service.search(query="example.com")
    assert result.total_count == 3
    names = [c.name for c in result.customers]
    assert names == ["Alice Johnson", "Jane Doe", "John Doe"]


def test_unified_query_deduplicates_matches(service: CustomerSearchService):
    # If query matches both name and email of someone, no duplicates are returned
    result = service.search(query="alice")
    assert result.total_count == 1
    assert result.customers[0].id == "C1"


def test_search_empty_results(service: CustomerSearchService):
    result = service.search(query="nonexistent_xyz")
    assert result.total_count == 0
    assert result.customers == []


def test_search_alphabetical_ordering(service: CustomerSearchService):
    # Query "es" matches José García (soluciones.mx) and María Fernández (empresa.es)
    result = service.search(query="es")
    names = [c.name for c in result.customers]
    assert names == sorted(names, key=lambda n: n.casefold())
    assert len(names) >= 2
