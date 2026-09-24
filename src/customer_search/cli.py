"""Command Line Interface for Customer Search."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from customer_search.exceptions import CustomerDataError, CustomerSearchValidationError
from customer_search.models import SearchResult
from customer_search.repository import InMemoryCustomerRepository
from customer_search.service import CustomerSearchService

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "customers.json"


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for customer search CLI."""
    parser = argparse.ArgumentParser(
        prog="customer-search",
        description="Search customer records by name or email with case-insensitive partial matching.",
    )
    parser.add_argument(
        "positional_query",
        nargs="?",
        default=None,
        help="Search term to search across name and email (shorthand for -q/--query).",
    )
    parser.add_argument(
        "-q",
        "--query",
        dest="query",
        default=None,
        help="Unified search query matching both name and email.",
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="name",
        default=None,
        help="Filter specifically by customer name.",
    )
    parser.add_argument(
        "-e",
        "--email",
        dest="email",
        default=None,
        help="Filter specifically by customer email.",
    )
    parser.add_argument(
        "-d",
        "--data",
        dest="data_path",
        default=str(DEFAULT_DATA_PATH),
        help=f"Path to JSON file containing customer records (default: {DEFAULT_DATA_PATH}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Format search output as JSON.",
    )
    return parser


def format_table(result: SearchResult) -> str:
    """Format search results as a human-readable text table."""
    if not result.customers:
        return f"No customers found matching {result.query}."

    headers = ["ID", "Name", "Email", "Phone", "Status"]
    rows = [
        [
            c.id,
            c.name,
            c.email,
            c.phone,
            "Active" if c.is_active else "Inactive",
        ]
        for c in result.customers
    ]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(cell)))

    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    formatted_rows = [
        " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        for row in rows
    ]

    output_lines = [
        header_line,
        separator_line,
        *formatted_rows,
        "",
        f"Found {result.total_count} customer(s) in {result.execution_time_ms:.2f} ms.",
    ]
    return "\n".join(output_lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Returns process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Resolve query from positional argument or -q flag
    search_query = args.query or args.positional_query

    try:
        # Load repository
        data_path = Path(args.data_path)
        if data_path.exists():
            repo = InMemoryCustomerRepository.from_json_file(data_path)
        else:
            raise CustomerDataError(f"Data file does not exist: {data_path}")

        service = CustomerSearchService(repo)
        result = service.search(
            query=search_query,
            name=args.name,
            email=args.email,
        )

        if args.output_json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(format_table(result))

        return 0

    except CustomerSearchValidationError as exc:
        print(f"Validation Error: {exc}", file=sys.stderr)
        return 2
    except CustomerDataError as exc:
        print(f"Data Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
