import pytest
import os
import sys
import re
from pathlib import Path
from utils.csv_parser import CSVParser, Employee
from reports.report_generator import ReportGenerator, PayoutReport

@pytest.fixture
def sample_csv_content():
    return """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60"""

@pytest.fixture
def sample_csv_file(tmp_path, sample_csv_content):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(sample_csv_content)
    return csv_file

def test_csv_parser(sample_csv_file):
    parser = CSVParser()
    employees = parser.parse_file(str(sample_csv_file))
    
    assert len(employees) == 3
    assert employees[0].name == "Alice Johnson"
    assert employees[0].hours_worked == 160
    assert employees[0].hourly_rate == 50

def test_csv_parser_with_different_rate_column(tmp_path):
    content = """id,email,name,department,hours_worked,rate
1,alice@example.com,Alice Johnson,Marketing,160,50"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(content)
    
    parser = CSVParser()
    employees = parser.parse_file(str(csv_file))
    
    assert len(employees) == 1
    assert employees[0].hourly_rate == 50

def test_csv_parser_file_not_found():
    parser = CSVParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("nonexistent.csv")

def test_csv_parser_permission_error(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("header\n")
    os.chmod(csv_file, 0o000)  # Remove all permissions
    try:
        parser = CSVParser()
        with pytest.raises(ValueError):
            parser.parse_file(str(csv_file))
    finally:
        os.chmod(csv_file, 0o644)  # Restore permissions so pytest can clean up

def test_payout_report():
    employees = [
        Employee(1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50),
        Employee(2, "bob@example.com", "Bob Smith", "Design", 150, 40),
        Employee(3, "carol@example.com", "Carol Williams", "Design", 170, 60)
    ]
    report = PayoutReport()
    result = report.generate(employees)
    expected = (
        "           name            hours  rate    payout\n"
        "Design\n"
        "-----------  Bob Smith         150    40  $   6000\n"
        "-----------  Carol Williams    170    60  $  10200\n"
        "                320  $  16200\n"
        "Marketing\n"
        "-----------  Alice Johnson     160    50  $   8000\n"
        "                160  $   8000\n"
        "                              $  24200"
    )
    def normalize(s):
        return re.sub(r'\s+', ' ', s.strip())
    assert [normalize(line) for line in result.splitlines()] == [normalize(line) for line in expected.splitlines()]

def test_report_generator_unknown_report():
    generator = ReportGenerator()
    with pytest.raises(ValueError, match="Unknown report type"):
        generator.generate_report("unknown", [])

def test_invalid_csv_format(tmp_path):
    content = """id,email,name,department,hours_worked\n1,alice@example.com,Alice Johnson,Marketing,160"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(content)
    parser = CSVParser()
    with pytest.raises(ValueError, match="No rate column found"):
        parser.parse_file(str(csv_file))

@pytest.mark.skipif(sys.platform != "win32", reason="Windows path test only relevant on Windows")
def test_csv_parser_with_windows_path(tmp_path, sample_csv_content):
    # Create a file with Windows-style path
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(sample_csv_content)
    windows_path = str(csv_file).replace("/", "\\")
    parser = CSVParser()
    employees = parser.parse_file(windows_path)
    assert len(employees) == 3
    assert employees[0].name == "Alice Johnson" 