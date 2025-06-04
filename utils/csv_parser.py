from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import os
import sys

@dataclass
class Employee:
    id: int
    email: str
    name: str
    department: str
    hours_worked: float
    hourly_rate: float

class CSVParser:
    RATE_COLUMN_VARIANTS = ['hourly_rate', 'rate', 'salary']
    ID_COLUMN_VARIANTS = ['id', 'ID', 'Id']
    EMAIL_COLUMN_VARIANTS = ['email', 'e-mail', 'Email']
    NAME_COLUMN_VARIANTS = ['name', 'Name']
    DEPT_COLUMN_VARIANTS = ['department', 'dept', 'Department']
    HOURS_COLUMN_VARIANTS = ['hours_worked', 'hours', 'Hours']

    def parse_file(self, file_path: str) -> List[Employee]:
        """Parse a CSV file and return a list of Employee objects."""
        employees = []
        file_path = os.path.normpath(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                header = f.readline().strip().split(',')
                header_map = {col.strip(): idx for idx, col in enumerate(header)}
                # Find actual column names in the file for each field
                id_col = self._find_column(header, self.ID_COLUMN_VARIANTS)
                email_col = self._find_column(header, self.EMAIL_COLUMN_VARIANTS)
                name_col = self._find_column(header, self.NAME_COLUMN_VARIANTS)
                dept_col = self._find_column(header, self.DEPT_COLUMN_VARIANTS)
                hours_col = self._find_column(header, self.HOURS_COLUMN_VARIANTS)
                rate_col = self._find_column(header, self.RATE_COLUMN_VARIANTS)
                if None in (id_col, email_col, name_col, dept_col, hours_col, rate_col):
                    raise ValueError(f"Missing required column in {file_path}")
                for line in f:
                    if not line.strip():
                        continue
                    values = line.strip().split(',')
                    if len(values) != len(header):
                        print(f"Warning: Skipping row with invalid number of columns in {file_path}: {values}", file=sys.stderr)
                        continue
                    try:
                        employee = Employee(
                            id=int(values[header_map[id_col]]),
                            email=values[header_map[email_col]],
                            name=values[header_map[name_col]],
                            department=values[header_map[dept_col]],
                            hours_worked=float(values[header_map[hours_col]]),
                            hourly_rate=float(values[header_map[rate_col]])
                        )
                        employees.append(employee)
                    except (ValueError, IndexError) as e:
                        print(f"Warning: Skipping row in {file_path} due to parse error: {values} ({str(e)})", file=sys.stderr)
                        continue
        except FileNotFoundError:
            raise
        except PermissionError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
        return employees

    def _find_column(self, header: List[str], variants: List[str]) -> str:
        for variant in variants:
            for col in header:
                if col.strip().lower() == variant.lower():
                    return col
        return None 