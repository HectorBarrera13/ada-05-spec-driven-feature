"""Performance benchmark test for NFR-01 (10,000 customer records < 100ms)."""

import time
import pytest
from customer_search.models import Customer
from customer_search.repository import InMemoryCustomerRepository
from customer_search.service import CustomerSearchService


def test_performance_10k_records():
    """Verify NFR-01: search across 10,000 records completes in < 100ms."""
    # Generate 10,000 synthetic customer records
    dataset = [
        Customer(
            id=f"CUST-{i:05d}",
            name=f"Customer Name {i}",
            email=f"user_{i}@domain.org",
            phone=f"+1-555-{i % 10000:04d}",
            is_active=(i % 2 == 0),
        )
        for i in range(10_000)
    ]

    repo = InMemoryCustomerRepository(dataset)
    service = CustomerSearchService(repo)

    # Measure search query
    start_time = time.perf_counter()
    result = service.search(query="Name 999")
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # Ensure results found and timing is within NFR-01 requirement (< 100ms)
    assert result.total_count >= 1
    assert elapsed_ms < 100.0, f"Search took {elapsed_ms:.2f} ms, exceeding 100ms limit"
    assert result.execution_time_ms < 100.0
