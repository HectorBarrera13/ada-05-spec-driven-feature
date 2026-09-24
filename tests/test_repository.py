"""Tests for customer repository."""

import json
from pathlib import Path
import pytest
from customer_search.exceptions import CustomerDataError
from customer_search.models import Customer
from customer_search.repository import InMemoryCustomerRepository


@pytest.fixture
def sample_customers() -> list[Customer]:
    return [
        Customer(id="C1", name="Alice Smith", email="alice@test.com", phone="111"),
        Customer(id="C2", name="Bob Jones", email="bob@test.com", phone="222"),
    ]


def test_in_memory_repository(sample_customers):
    repo = InMemoryCustomerRepository(sample_customers)
    assert len(repo.get_all()) == 2
    repo.add(Customer(id="C3", name="Charlie Brown", email="charlie@test.com", phone="333"))
    assert len(repo.get_all()) == 3


def test_from_json_file(tmp_path: Path):
    file_path = tmp_path / "customers.json"
    data = [
        {"id": "C10", "name": "Diana Ross", "email": "diana@test.com", "phone": "444", "is_active": True}
    ]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repo = InMemoryCustomerRepository.from_json_file(file_path)
    customers = repo.get_all()
    assert len(customers) == 1
    assert customers[0].name == "Diana Ross"


def test_from_json_file_not_found(tmp_path: Path):
    non_existent = tmp_path / "missing.json"
    with pytest.raises(CustomerDataError, match="not found"):
        InMemoryCustomerRepository.from_json_file(non_existent)


def test_from_json_file_malformed_json(tmp_path: Path):
    file_path = tmp_path / "broken.json"
    file_path.write_text("{ broken json ]", encoding="utf-8")
    with pytest.raises(CustomerDataError, match="Malformed JSON"):
        InMemoryCustomerRepository.from_json_file(file_path)


def test_from_json_file_invalid_schema(tmp_path: Path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text(json.dumps([{"id": "C1"}]), encoding="utf-8")  # missing name and email
    with pytest.raises(CustomerDataError, match="Invalid customer record"):
        InMemoryCustomerRepository.from_json_file(file_path)
