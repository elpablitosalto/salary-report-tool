#!/usr/bin/env python3
import argparse
import os
import sys
from typing import List
from reports.report_generator import ReportGenerator
from utils.csv_parser import CSVParser

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate salary reports from CSV files')
    parser.add_argument('files', nargs='+', help='CSV files to process')
    parser.add_argument('--report', required=True, help='Type of report to generate')
    return parser.parse_args()

def validate_files(files: List[str]) -> List[str]:
    """Validate that all files exist and are readable."""
    valid_files = []
    for file_path in files:
        normalized_path = os.path.normpath(file_path)
        if not os.path.exists(normalized_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            continue
        if not os.access(normalized_path, os.R_OK):
            print(f"Error: Cannot read file: {file_path}", file=sys.stderr)
            continue
        valid_files.append(normalized_path)
    return valid_files

def main() -> None:
    try:
        args = parse_args()
        
        # Validate files
        valid_files = validate_files(args.files)
        if not valid_files:
            print("Error: No valid files to process", file=sys.stderr)
            sys.exit(1)
        
        # Initialize CSV parser and read all files
        csv_parser = CSVParser()
        employees_data = []
        
        for file_path in valid_files:
            try:
                employees_data.extend(csv_parser.parse_file(file_path))
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
                continue
        
        if not employees_data:
            print("Error: No valid employee data found in any file", file=sys.stderr)
            sys.exit(1)
        
        # Generate report
        report_generator = ReportGenerator()
        try:
            report = report_generator.generate_report(args.report, employees_data)
            print(report)
        except ValueError as e:
            print(f"Error generating report: {str(e)}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 