from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class MainClient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EndClient(models.Model):
    name = models.CharField(max_length=100)
    main_client = models.ForeignKey(MainClient, on_delete=models.CASCADE, related_name='end_clients')

    def __str__(self):
        return self.name

class MigrantType(models.Model):
    migrant_name = models.CharField(max_length=50)

    def __str__(self):
        return self.migrant_name




class RoleSow(models.Model):
    name = models.CharField(max_length=100)  # Role/SOW name (e.g., Developer, Manager, etc.)
    description = models.TextField(blank=True, null=True)  # Role-specific descriptions
    main_client = models.ForeignKey(
        MainClient,
        on_delete=models.CASCADE,
        related_name="rolesows",
        blank=True,
        null=True,

    )

    def __str__(self):
        return f"{self.name} ({self.main_client.name})"



class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_profile")
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    main_client = models.ForeignKey(MainClient, on_delete=models.SET_NULL, null=True, blank=True)
    end_clients = models.ManyToManyField(EndClient, related_name="managers", blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.main_client})"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile", blank=True, null=True)
    employee_serial_id = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    main_account = models.ForeignKey(MainClient, on_delete=models.SET_NULL, null=True, blank=True)
    end_client = models.ForeignKey(EndClient, on_delete=models.SET_NULL, null=True, blank=True)
    client_account_manager = models.ForeignKey(Manager, on_delete=models.SET_NULL,blank=True, null=True)
    pass_type = models.ForeignKey(MigrantType, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField(blank=True, null=True)
    sow_start_date = models.DateField(blank=True, null=True)
    sow_end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    work_role = models.CharField(max_length=200, blank=True, null=True)
    role_sow = models.ForeignKey(RoleSow, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    is_pmo = models.BooleanField(default=False)
    shift_hours_day = models.IntegerField(default=8)
    shift_days_week = models.FloatField(default=5)
    yearly_annual_leave_entitlement = models.IntegerField(default=14)
    yearly_sick_leave_entitlement = models.IntegerField(default=14)
    ot_allowed = models.BooleanField(default=False)
    ph_allowed = models.BooleanField(default=False)
    country_choices = [
        ("Singapore", "Singapore"),
        ("India", "India"),
        ("Malaysia", "Malaysia"),
        ("Philippines", "Philippines"),
    ]

    location = models.CharField(
        max_length=50,
        choices=country_choices,
        default="Singapore"
    )

    def __str__(self):
        return self.full_name


class TaskType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_base = models.BooleanField(default=True)  # Distinguish between base and employee-specific types
    role_sow = models.ForeignKey(RoleSow, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_types")

    def __str__(self):
        return self.name



class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    associated_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    role_sow = models.ForeignKey(RoleSow, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    is_base = models.BooleanField(default=True)  # Shared for all users or specific to one
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TimesheetPeriod(models.Model):
    PERIOD_TYPE_CHOICES = [
        ('WEEK', 'Weekly'),
        ('MONTH', 'Monthly'),
    ]

    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE_CHOICES)
    start_date = models.DateField()  # Start of the week/month
    end_date = models.DateField()  # End of the week/month
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_period_type_display()} ({self.start_date} to {self.end_date})"


class TimesheetEntry(models.Model):
    JOB_TYPE_CHOICES = [
        ('WORK', 'Work'),
        ('Leave', 'Leave'),
        ('Public Holiday', 'Public Holiday'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='WORK')
    work_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ot_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_ot = models.BooleanField(default=False)
    break_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    timesheet_period = models.ForeignKey(TimesheetPeriod, on_delete=models.CASCADE, related_name="entries")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ("employee", "date", "task", "job_type")

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.job_type})"

from django.db import models
from django.utils import timezone

# --- Existing imports assumed ---
# from .models import Employee, TimesheetPeriod


class TimesheetSubmission(models.Model):
    """
    Represents a single employee’s timesheet submission for a specific period (month or week).
    One record per employee per period.
    """
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    employee = models.ForeignKey(
    Employee, on_delete=models.CASCADE, related_name="timesheet_submissions"
    )
    period = models.ForeignKey(
        TimesheetPeriod, on_delete=models.CASCADE, related_name="timesheet_submissions"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    reviewed_by = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reviewed_timesheets"
    )
    reviewer_comment = models.TextField(blank=True, null=True)
    employee_remark = models.TextField(blank=True, null=True)

    # optional system fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "period")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee.full_name} - {self.period} ({self.status})"

    def mark_submitted(self):
        """Mark the timesheet as submitted by employee."""
        self.status = "SUBMITTED"
        self.submitted_at = timezone.now()
        self.save(update_fields=["status", "submitted_at", "updated_at"])

    def mark_approved(self, manager, comment=None):
        """Manager approves the submission."""
        self.status = "APPROVED"
        self.reviewed_at = timezone.now()
        self.reviewed_by = manager
        self.reviewer_comment = comment or ""
        self.save(update_fields=["status", "reviewed_at", "reviewed_by", "reviewer_comment", "updated_at"])

    def mark_rejected(self, manager, comment):
        """Manager rejects with feedback."""
        self.status = "REJECTED"
        self.reviewed_at = timezone.now()
        self.reviewed_by = manager
        self.reviewer_comment = comment
        self.save(update_fields=["status", "reviewed_at", "reviewed_by", "reviewer_comment", "updated_at"])

    def reset_to_draft(self):
        """Used when employee edits after rejection."""
        self.status = "DRAFT"
        self.save(update_fields=["status", "updated_at"])

class TimesheetApprovalLog(models.Model):
    """
    Immutable audit log for each submission action:
    SUBMIT, APPROVE, REJECT, RESUBMIT, etc.
    """
    ACTION_CHOICES = [
        ("SAVE_DRAFT", "Save Draft"),
        ("SUBMIT", "Submit"),
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
        ("RESUBMIT", "Resubmit"),
    ]

    submission = models.ForeignKey(
        TimesheetSubmission,
        on_delete=models.CASCADE,
        related_name="logs"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approval_logs"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.submission} - {self.action} by {self.actor or 'System'}"

class LeaveRecord(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CANCELLED", "Cancelled"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_records")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    date = models.DateField()  # One row per day
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="APPROVED")
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("employee", "date", "leave_type")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} on {self.date} ({self.status})"

class MedicalCertificate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="medical_certificates")
    period = models.ForeignKey(TimesheetPeriod, on_delete=models.CASCADE, null=True, blank=True)
    month = models.CharField(max_length=7)  # "2025-02"
    file = models.FileField(upload_to="medical_certificates/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month} - {self.file.name}"


class PublicHoliday(models.Model):
    holiday_name = models.CharField(max_length=200)
    holiday_date = models.DateField()
    COUNTRY_CHOICES = [
        ("Singapore", "Singapore"),
        ("India", "India"),
        ("Malaysia", "Malaysia"),
        ("Philippines", "Philippines"),
    ]
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default="Singapore")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["holiday_date"]
        constraints = [
            models.UniqueConstraint(fields=["holiday_date", "country"], name="unique_holiday_per_country")
        ]


    def __str__(self):
        return f"{self.holiday_name} ({self.holiday_date} - {self.country})"


class LeaveCycle(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="leave_cycles"
    )

    cycle_start = models.DateField()
    cycle_end = models.DateField()

    # Annual leave (from employee.yearly_annual_leave_entitlement)
    annual_leave_entitled = models.DecimalField(max_digits=5, decimal_places=2)
    annual_leave_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    annual_leave_used = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    annual_leave_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Sick leave (from employee.yearly_sick_leave_entitlement)
    medical_leave_entitled = models.DecimalField(max_digits=5, decimal_places=2)
    medical_leave_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    medical_leave_used = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    medical_leave_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "cycle_start")

    def __str__(self):
        return f"{self.employee.full_name}: {self.cycle_start} → {self.cycle_end}"

from django.db import models
from django.contrib.auth.models import User

class LeaveAdjustment(models.Model):
    ADJUSTMENT_TYPE = [
        ("ANNUAL", "Annual Leave"),
        ("MEDICAL", "Medical Leave"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_adjustments"
    )

    cycle = models.ForeignKey(
        LeaveCycle,
        on_delete=models.CASCADE,
        related_name="adjustments"
    )

    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPE)

    # Positive (+) or Negative (-) adjustments
    days = models.DecimalField(max_digits=5, decimal_places=1)

    reason = models.TextField(blank=True, null=True)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_adjustments_approved"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee.full_name} – {self.adjustment_type} ({self.days})"


class Claim(models.Model):
    STATUS_CHOICES = [
        ("SUBMITTED", "Submitted"),
        ("REJECTED", "Rejected"),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="claims"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    description = models.TextField()   # No need for claim type
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUBMITTED"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    rejected_by = models.ForeignKey(
        Manager,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rejected_claims"
    )
    rejected_comment = models.TextField(blank=True, null=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Claim {self.id} – {self.employee.full_name}"

class ClaimAttachment(models.Model):
    claim = models.ForeignKey(
        Claim, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="claim_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Claim {self.claim.id}"


class LeaveImport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "date", "leave_type")


class AssetInventory(models.Model):
    asset_type = models.CharField(
        max_length=50,
        help_text="Laptop, Headphones, Mouse, Keyboard, Monitor"
    )
    asset_color = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    serial_number = models.CharField(
        max_length=100, blank=True, null=True)

    purchased_at = models.CharField(
        max_length=200,null=True, blank=True,
    )
    optional_description = models.TextField(blank=True, null=True)

    purchased_date = models.DateField(
        blank=True,
        null=True
    )

    last_repaired_on = models.DateField(
        blank=True,
        null=True
    )
    last_repair_details = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_type} - {self.serial_number}"


class Asset(models.Model):
    inventory = models.ForeignKey(
        AssetInventory,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="assets"
    )

    received_on = models.DateField()
    returned_on = models.DateField(blank=True, null=True)

    is_with_employee = models.BooleanField(default=True)

    remarks = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory.asset_type} → {self.employee.full_name}"

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CANCELLED", "Cancelled"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_applications")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    # optional for future (0.5 support later)
    duration = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)

    reason = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    applied_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    admin_comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-applied_on"]

    def __str__(self):
        return f"{self.employee.full_name}: {self.start_date} → {self.end_date}"
