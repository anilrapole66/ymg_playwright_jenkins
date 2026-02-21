import os
import sys
from datetime import date, timedelta

# ✅ Set up Django before importing any models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_portal.settings")

import django
django.setup()


import openpyxl
from datetime import datetime
from employees.models import Employee, LeaveImport, LeaveType

def import_leave_data(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)

    # Sheet names assumed: "Annual" and "Medical"
    sheets = {
        "AL": "ANNUAL",
        "ML": "MEDICAL"
    }

    # Preload LeaveType references
    LT_ANNUAL = LeaveType.objects.get(name="Annual Leave")
    LT_HALF_ANNUAL = LeaveType.objects.get(name="Half Annual Leave")
    LT_MEDICAL = LeaveType.objects.get(name="Medical Leave")
    LT_HALF_MEDICAL = LeaveType.objects.get(name="Half Medical Leave")

    created_count = 0
    skipped_count = 0

    for sheet_name, leave_category in sheets.items():
        sheet = wb[sheet_name]

        for row in sheet.iter_rows(min_row=2):  # skip header
            emp_name = row[4].value      # Column E
            date_val = row[10].value     # Column K
            leave_val = row[11].value    # Column L (1 or 0.5)

            if not emp_name or not date_val or not leave_val:
                continue

            # Normalize employee name
            emp_name_clean = str(emp_name).strip()

            # Find employee
            print(emp_name_clean, "ccccccccc")
            employee = Employee.objects.filter(full_name__iexact=emp_name_clean).first()
            if not employee:
                print(f"Employee not found: {emp_name}")
                skipped_count += 1
                continue

            # Parse date
            if isinstance(date_val, datetime):
                date_val = date_val.date()

            # Determine LeaveType
            if leave_category == "ANNUAL":
                leave_type = LT_HALF_ANNUAL if leave_val == 0.5 else LT_ANNUAL
            else:
                leave_type = LT_HALF_MEDICAL if leave_val == 0.5 else LT_MEDICAL

            # Create LeaveImport entry
            obj, created = LeaveImport.objects.get_or_create(
                employee=employee,
                date=date_val,
                leave_type=leave_type
            )

            if created:
                created_count += 1
            else:
                skipped_count += 1

    print(f"Imported: {created_count} records, Skipped: {skipped_count} (duplicates)")


if __name__ == "__main__":
    import_leave_data("/home/jai/Downloads/villa.xlsx")