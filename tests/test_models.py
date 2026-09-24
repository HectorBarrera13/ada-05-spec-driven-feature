"""Tests for Customer and SearchResult domain models."""

import pytest
from customer_search.models import Customer, SearchResult


def test_customer_creation():
    customer = Customer(
        id="CUST-001",
        name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0100",
        is_active=True,
    )
    assert customer.id == "CUST-001"
    assert customer.name == "Alice Smith"
    assert customer.email == "alice@example.com"
    assert customer.phone == "+1-555-0100"
    assert customer.is_active is True


def test_customer_is_immutable():
    customer = Customer(
        id="CUST-001",
        name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0100",
    )
    with pytest.raises(Exception):
        customer.name = "Bob"  # type: ignore


def test_customer_validation():
    with pytest.raises(ValueError, match="Customer id"):
        Customer(id="", name="Valid", email="valid@example.com", phone="123")

    with pytest.raises(ValueError, match="Customer name"):
        Customer(id="C1", name="", email="valid@example.com", phone="123")

    with pytest.raises(ValueError, match="Customer email"):
        Customer(id="C1", name="Valid", email="", phone="123")


def test_customer_serialization():
    data = {
        "id": "CUST-002",
        "name": "Bob Jones",
        "email": "bob@example.com",
        "phone": "+1-555-0200",
        "is_active": False,
    }
    customer = Customer.from_dict(data)
    assert customer.name == "Bob Jones"
    assert customer.is_active is False
    assert customer.to_dict() == data


def test_search_result_serialization():
    customer = Customer(
        id="CUST-001",
        name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0100",
    )
    result = SearchResult(
        customers=[customer],
        total_count=1,
        query="alice",
        execution_time_ms=1.25,
    )
    assert result.total_count == 1
    assert result.query == "alice"
    assert len(result.customers) == 1
    serialized = result.to_dict()
    assert serialized["total_count"] == 1
    assert serialized["execution_time_ms"] == 1.25
    assert serialized["customers"][0]["id"] == "CUST-001"
