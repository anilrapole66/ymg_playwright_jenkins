# employees/leave_service.py
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from employees.models import LeaveCycle, TimesheetEntry, LeaveApplication
import math
# -----------------------------------------------------------
# 1. CREATE OR FETCH ACTIVE CYCLE
# -----------------------------------------------------------

def get_calendar_cycle(year=None):
    if not year:
        year = timezone.now().year

    return {
        "start": date(year, 1, 1),
        "end": date(year, 12, 31)
    }

def is_half_day_leave(leave):
    """
    Determines if a leave is half-day based on leave type name.
    """
    if not leave.leave_type:
        return False

    name = leave.leave_type.name.lower()
    return "half" in name


def iter_working_dates(start_date, end_date):
    """
    Yield dates in [start_date, end_date] that are weekdays (Mon-Fri).
    """
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Mon=0 ... Sun=6
            yield current
        current += timedelta(days=1)


def working_days_between(start_date, end_date):
    """
    Count weekdays (Mon-Fri) in [start_date, end_date].
    """
    if not start_date or not end_date or start_date > end_date:
        return 0
    return sum(1 for _ in iter_working_dates(start_date, end_date))


def effective_leave_days(start_date, end_date, is_half_day=False):
    """
    Leave days excluding weekends. Half-day leave on working dates counts as 0.5.
    """
    days = working_days_between(start_date, end_date)
    if is_half_day:
        return 0.5 if days > 0 else 0.0
    return float(days)

def get_approved_leave_days(employee, cycle_start, cycle_end):
    """
    Returns total approved leave days for an employee within a cycle.
    Handles full-day and half-day leaves.
    """

    leaves = LeaveApplication.objects.filter(
        employee=employee,
        status="APPROVED",
        start_date__lte=cycle_end,
        end_date__gte=cycle_start
    )

    total_days = 0.0

    for leave in leaves:
        # clip leave range to cycle
        start = max(leave.start_date, cycle_start)
        end = min(leave.end_date, cycle_end)

        total_days += effective_leave_days(
            start,
            end,
            is_half_day=is_half_day_leave(leave),
        )

    return total_days

def get_or_create_active_cycle(employee):
    doj = employee.date_of_joining
    today = date.today()

    if doj > today:
        cycle_start = doj
        cycle_end = doj + relativedelta(years=1) - relativedelta(days=1)
    elif doj < today:
        cycle_start = doj
        cycle_end = doj + relativedelta(years=1) - relativedelta(days=1)

        # Advance cycle until today fits inside
        while not (cycle_start <= today <= cycle_end):
            cycle_start += relativedelta(years=1)
            cycle_end = cycle_start + relativedelta(years=1) - relativedelta(days=1)

    cycle, _ = LeaveCycle.objects.get_or_create(
        employee=employee,
        cycle_start=cycle_start,
        defaults={
            "cycle_end": cycle_end,
            "annual_leave_entitled": employee.yearly_annual_leave_entitlement,
            "medical_leave_entitled": employee.yearly_sick_leave_entitlement,
        }
    )
    return cycle


# -----------------------------------------------------------
# 2. CALCULATE EARNED LEAVE
# -----------------------------------------------------------

def floor_to_half_day(value):
    """Floor value to nearest 0.5 (downwards)."""
    return math.floor(value * 2) / 2.0

def calculate_earned_leave(cycle):
    today = date.today()
    
    months_passed = (today.year - cycle.cycle_start.year) * 12 + \
                    (today.month - cycle.cycle_start.month)

    if today.day < cycle.cycle_start.day:
        months_passed -= 1

    months_passed = max(months_passed, 0)
    if cycle.annual_leave_entitled != cycle.employee.yearly_annual_leave_entitlement:
        cycle.annual_leave_entitled = cycle.employee.yearly_annual_leave_entitlement
        cycle.medical_leave_entitled = cycle.employee.yearly_sick_leave_entitlement
        cycle.save()
    raw_annual = (cycle.annual_leave_entitled / 12) * months_passed
    raw_medical = (cycle.medical_leave_entitled / 12) * months_passed
    cycle.annual_leave_earned = floor_to_half_day(raw_annual)
    cycle.medical_leave_earned = floor_to_half_day(raw_medical)


# -----------------------------------------------------------
# 3. CALCULATE USED LEAVE FOR ENTIRE CYCLE
# -----------------------------------------------------------
def calculate_used_leave(cycle, employee):
    # ------------------------------
    # 1. EXISTING TIMESHEET LEAVE
    # ------------------------------
    ts_leaves = TimesheetEntry.objects.filter(
        employee=employee,
        job_type="Leave",
        date__range=(cycle.cycle_start, cycle.cycle_end)
    ).select_related("leave_type")

    annual_used = 0
    medical_used = 0

    for entry in ts_leaves:
        lt = entry.leave_type.name.lower().strip()

        if lt in ("annual", "annual leave", "al"):
            annual_used += 1
        elif lt in ("half annual", "half annual leave", "half day annual leave"):
            annual_used += 0.5
        elif lt in ("medical", "medical leave", "sick", "mc"):
            medical_used += 1
        elif lt in ("half medical", "half medical leave", "half sick leave", "half day medical leave"):
            medical_used += 0.5

    # ------------------------------
    # 2. IMPORTED HISTORICAL LEAVE
    # ------------------------------
    from employees.models import LeaveImport

    imported = LeaveImport.objects.filter(
        employee=employee,
        date__range=(cycle.cycle_start, cycle.cycle_end)
    )
    for record in imported:
        lt = record.leave_type.name.lower().strip()

        if lt in ("annual", "annual leave", "al"):
            annual_used += 1
        elif lt in ("half annual", "half annual leave", "half day annual leave"):
            annual_used += 0.5
        elif lt in ("medical", "medical leave", "sick", "mc"):
            medical_used += 1
        elif lt in ("half medical", "half medical leave", "half sick leave", "half day medical leave"):
            medical_used += 0.5

    # ------------------------------
    # 3. SAVE TOTALS
    # ------------------------------
    cycle.annual_leave_used = annual_used
    cycle.medical_leave_used = medical_used


from django.db.models import Sum
from employees.models import LeaveAdjustment

def update_leave_cycle(employee):
    cycle = get_or_create_active_cycle(employee)

    # Pure earned + used
    calculate_earned_leave(cycle)
    calculate_used_leave(cycle, employee)

    # ---------------------------------------------------
    # NEW: Fetch adjustments for this cycle
    # ---------------------------------------------------
    annual_adjustments = float(
        LeaveAdjustment.objects.filter(
            employee=employee,
            cycle=cycle,
            adjustment_type="ANNUAL"
        ).aggregate(total=Sum("days"))["total"] or 0
    )

    medical_adjustments = float(
        LeaveAdjustment.objects.filter(
            employee=employee,
            cycle=cycle,
            adjustment_type="MEDICAL"
        ).aggregate(total=Sum("days"))["total"] or 0
    )

    cycle.annual_leave_balance = (
            float(cycle.annual_leave_earned)
            - float(cycle.annual_leave_used)
            + annual_adjustments
    )

    cycle.medical_leave_balance = (
            float(cycle.medical_leave_earned)
            - float(cycle.medical_leave_used)
            + medical_adjustments
    )

    cycle.save()

    return cycle
