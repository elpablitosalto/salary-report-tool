# Salary Report Tool

A command-line tool for generating salary reports from CSV files containing employee data.

## Features

- Read employee data from CSV files
- Generate salary reports
- Support for different rate column names (hourly_rate, rate, salary)
- Extensible architecture for adding new report types

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py ./csv/data1.csv ./csv/data2.csv ./csv/data3.csv --report payout
```

The tool will read the specified CSV files and generate a report of the specified type.

### CSV File Format

The input CSV files should have the following columns:
- id
- email
- name
- department
- hours_worked
- hourly_rate (or rate, or salary)

Example:
```csv
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
```

## Adding New Reports

To add a new report type:

1. Create a new class in `reports/report_generator.py` that inherits from the `Report` abstract base class
2. Implement the `generate` method
3. Register the new report in the `ReportGenerator` class's `__init__` method

Example:
```python
class NewReport(Report):
    def generate(self, employees: List[Employee]) -> str:
        # Implement report generation logic
        pass

# In ReportGenerator.__init__:
self._reports = {
    'payout': PayoutReport(),
    'new_report': NewReport()
}
```

## Running Tests

Run tests with coverage:
```bash
pytest --cov=.
```

## Requirements

- Python 3.6+
- pytest (for testing)
- pytest-cov (for test coverage) 