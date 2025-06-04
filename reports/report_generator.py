from typing import List, Dict, Any
from abc import ABC, abstractmethod
from utils.csv_parser import Employee
from collections import defaultdict

class Report(ABC):
    @abstractmethod
    def generate(self, employees: List[Employee]) -> str:
        pass

class PayoutReport(Report):
    def generate(self, employees: List[Employee]) -> str:
        """Generate a payout report grouped by department with formatted output."""
        # Group employees by department
        departments = defaultdict(list)
        for emp in employees:
            departments[emp.department].append(emp)
        
        # Formatting
        name_w = max(len(emp.name) for emp in employees) + 2
        dept_w = max(len(dept) for dept in departments) + 2
        hours_w = 5
        rate_w = 4
        payout_w = 8
        
        lines = []
        header = f"{'':<{dept_w}}{'name':<{name_w}}{'hours':>{hours_w}}  {'rate':>{rate_w}}  {'payout':>{payout_w}}"
        lines.append(header)
        
        grand_total = 0
        for dept, emps in sorted(departments.items()):
            lines.append(f"{dept}")
            dept_hours = 0
            dept_payout = 0
            for emp in emps:
                payout = emp.hours_worked * emp.hourly_rate
                dept_hours += emp.hours_worked
                dept_payout += payout
                lines.append(f"{'-'*dept_w}  {emp.name:<{name_w}}{int(emp.hours_worked):>{hours_w}}  {int(emp.hourly_rate):>{rate_w}}  ${int(payout):>{payout_w-1}}")
            # Department totals (align under the corresponding columns)
            lines.append(f"{'':<{dept_w}}{'':<{name_w}}{int(dept_hours):>{hours_w}}  {'':>{rate_w}}  ${int(dept_payout):>{payout_w-1}}")
            grand_total += dept_payout
        # Calculate payout column start (in characters)
        payout_col_pos = dept_w + name_w + hours_w + 2 + rate_w + 2  # 2 spaces after hours and rate
        total_str = f"${int(grand_total):>{payout_w-1}}"
        total_line = ' ' * payout_col_pos + total_str
        lines.append(total_line)
        return "\n".join(lines)

class ReportGenerator:
    def __init__(self):
        self._reports = {
            'payout': PayoutReport()
        }
    
    def generate_report(self, report_type: str, employees: List[Employee]) -> str:
        """Generate a report of the specified type."""
        if report_type not in self._reports:
            raise ValueError(f"Unknown report type: {report_type}")
        
        return self._reports[report_type].generate(employees) 