"""Tests for Customer Search CLI interface."""

import json
from pathlib import Path
import pytest
from customer_search.cli import main


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    sample = [
        {"id": "C1", "name": "Alice Johnson", "email": "alice@example.com", "phone": "111", "is_active": True},
        {"id": "C2", "name": "Bob Smith", "email": "bob@example.com", "phone": "222", "is_active": False},
        {"id": "C3", "name": "José García", "email": "jose@example.es", "phone": "333", "is_active": True},
    ]
    file = tmp_path / "customers.json"
    file.write_text(json.dumps(sample), encoding="utf-8")
    return file


def test_cli_positional_search(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["alice", "-d", str(data_file)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Alice Johnson" in captured.out
    assert "Found 1 customer(s)" in captured.out


def test_cli_json_output(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["--query", "example.com", "--data", str(data_file), "--json"])
    assert exit_code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["total_count"] == 2
    assert len(data["customers"]) == 2
    assert data["customers"][0]["name"] == "Alice Johnson"


def test_cli_name_flag(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["-n", "jose", "-d", str(data_file)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "José García" in captured.out


def test_cli_email_flag(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["-e", "example.es", "-d", str(data_file)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "José García" in captured.out


def test_cli_zero_matches(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["nonexistent", "-d", str(data_file)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "No customers found matching" in captured.out


def test_cli_validation_error_empty(data_file: Path, capsys: pytest.CaptureFixture):
    # No search parameters passed
    exit_code = main(["-d", str(data_file)])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Validation Error" in captured.err


def test_cli_validation_error_short(data_file: Path, capsys: pytest.CaptureFixture):
    exit_code = main(["x", "-d", str(data_file)])
    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Validation Error" in captured.err
    assert "too short" in captured.err


def test_cli_data_file_missing(capsys: pytest.CaptureFixture):
    exit_code = main(["alice", "-d", "/nonexistent/path/customers.json"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Data Error" in captured.err
