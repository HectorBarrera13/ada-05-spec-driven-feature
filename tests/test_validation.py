"""Tests for search validation rules and exceptions."""

import pytest
from customer_search.exceptions import CustomerSearchValidationError
from customer_search.models import Customer
from customer_search.repository import InMemoryCustomerRepository
from customer_search.service import CustomerSearchService
from customer_search.validation import validate_search_params, validate_search_term


def test_validate_search_term_valid():
    assert validate_search_term("ab") == "ab"
    assert validate_search_term("  alice  ") == "alice"
    assert validate_search_term("123") == "123"


def test_validate_search_term_empty():
    with pytest.raises(CustomerSearchValidationError, match="must not be empty"):
        validate_search_term("")

    with pytest.raises(CustomerSearchValidationError, match="must not be empty"):
        validate_search_term(None)


def test_validate_search_term_whitespace():
    with pytest.raises(CustomerSearchValidationError, match="must not consist solely of whitespace"):
        validate_search_term("   ")

    with pytest.raises(CustomerSearchValidationError, match="must not consist solely of whitespace"):
        validate_search_term("\t\n")


def test_validate_search_term_too_short():
    with pytest.raises(CustomerSearchValidationError, match="too short"):
        validate_search_term("a")

    with pytest.raises(CustomerSearchValidationError, match="too short"):
        validate_search_term(" x ")


def test_validate_search_params_no_parameters():
    with pytest.raises(CustomerSearchValidationError, match="At least one search parameter"):
        validate_search_params(query=None, name=None, email=None)


def test_validate_search_params_combination():
    q, n, e = validate_search_params(query="al", name="bob", email=None)
    assert q == "al"
    assert n == "bob"
    assert e is None


def test_service_validation_integration():
    repo = InMemoryCustomerRepository()
    service = CustomerSearchService(repo)

    with pytest.raises(CustomerSearchValidationError, match="At least one search parameter"):
        service.search()

    with pytest.raises(CustomerSearchValidationError, match="too short"):
        service.search(query="z")

    with pytest.raises(CustomerSearchValidationError, match="whitespace"):
        service.search(name="   ")
