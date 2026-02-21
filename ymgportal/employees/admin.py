from django.contrib import admin
from .models import *

@admin.register(MainClient)
class MainClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(EndClient)
class EndClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_client')
    search_fields = ('name',)
    list_filter = ('main_client',)


@admin.register(MigrantType)
class MigrantTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'migrant_name')
    search_fields = ('migrant_name',)



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee_serial_id',
        'full_name',
        'email',
        'main_account',
        'work_role',
        'date_of_birth',
        'date_of_joining',
        'sow_start_date',
        'sow_end_date',
        'is_active',
    )
    search_fields = ('employee_serial_id', 'full_name', 'email')
    list_filter = ('main_account', 'end_client', 'pass_type', 'is_active')
    actions = ('bulk_inactivate',)

    def bulk_inactivate(self, request, queryset):
        for emp in queryset:
            if emp.is_active:
                emp.is_active = False
                emp.save(update_fields=["is_active"])
                if emp.user and emp.user.is_active:
                    emp.user.is_active = False
                    emp.user.save(update_fields=["is_active"])
        self.message_user(request, f"{queryset.count()} employee(s) set to inactive.")
    bulk_inactivate.short_description = "Mark selected employees as inactive"

from .models import RoleSow, Task

@admin.register(RoleSow)
class RoleSowAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'main_client')
    search_fields = ('name', 'main_client__name')
    list_filter = ('main_client',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'role_sow', 'associated_employee', 'is_base', 'is_active', 'created_on')
    search_fields = ('name', 'type__name', 'role_sow__name')
    list_filter = ('is_base', 'role_sow')


from .models import TimesheetEntry, TaskType, LeaveType, TimesheetPeriod

@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id','employee', 'date', 'job_type', 'task', 'task_type',
        'work_hours', 'ot_hours', 'break_hours', 'leave_type', 'timesheet_period'
    )
    search_fields = ('employee__full_name', 'task__name', 'task_type__name', 'leave_type__name')
    list_filter = ('job_type', 'timesheet_period', 'employee', 'task_type', 'leave_type', 'task')
    date_hierarchy = 'date'


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_sow', 'is_base')
    search_fields = ('name', 'role_sow__name')
    list_filter = ('is_base', 'role_sow')


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_paid', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_paid', 'is_active')

@admin.register(TimesheetPeriod)
class TimesheetPeriodAdmin(admin.ModelAdmin):
    list_display = ('period_type', 'start_date', 'end_date', 'created_at', 'updated_at')
    list_filter = ('period_type', 'start_date', 'end_date')
    date_hierarchy = 'start_date'
    search_fields = ()


@admin.register(TimesheetSubmission)
class TimesheetSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'period', 'status', 'submitted_at', 'reviewed_by')
    search_fields = ('employee__full_name', 'status')
    list_filter = ('status', 'submitted_at')

@admin.register(TimesheetApprovalLog)
class TimesheetApprovalLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'action', 'actor', 'timestamp')
    search_fields = ('action', 'actor__username', 'submission__employee__full_name')
    list_filter = ('action', 'timestamp')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'main_client', 'is_active')
    search_fields = ('full_name', 'email')
    list_filter = ('main_client', 'is_active')



@admin.register(PublicHoliday)
class PublicHolidayAdmin(admin.ModelAdmin):
    list_display = ('id', 'holiday_name', 'holiday_date', 'country', 'is_active')
    list_filter = ('country', 'is_active', 'holiday_date')
    search_fields = ('holiday_name', 'country')
    ordering = ('holiday_date',)


@admin.register(LeaveRecord)
class LeaveRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'date', 'status', 'applied_on', 'approved_by')
    search_fields = ('employee__full_name', 'leave_type__name', 'reason')
    list_filter = ('status', 'leave_type', 'date')
    date_hierarchy = 'date'


@admin.register(MedicalCertificate)
class MedicalCertificateAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'uploaded_at', 'file')
    search_fields = ('employee__full_name', 'month')
    list_filter = ('month',)


@admin.register(LeaveCycle)
class LeaveCycleAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'cycle_start',
        'cycle_end',
        'annual_leave_entitled',
        'annual_leave_balance',
        'medical_leave_entitled',
        'medical_leave_balance',
    )
    search_fields = ('employee__full_name',)
    list_filter = ('cycle_start', 'cycle_end')

@admin.register(LeaveAdjustment)
class LeaveAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'adjustment_type', 'days', 'reason', 'created_at')
    search_fields = ('employee__full_name', 'reason')
    list_filter = ('adjustment_type', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(LeaveImport)
class LeaveImportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'leave_type', 'created_at')
    search_fields = ('employee__full_name', 'leave_type__name')
    list_filter = ('leave_type', 'date')
    date_hierarchy = 'date'


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    search_fields = ('employee__full_name', 'employee__email', 'leave_type__name')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    date_hierarchy = 'start_date'


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'start_date',
        'end_date',
        'amount',
        'status',
        'submitted_at',
    )

    search_fields = (
        'employee__full_name',
        'employee__email',
        'description',
    )

    list_filter = (
        'status',
        'start_date',
        'submitted_at',
    )
    date_hierarchy = 'submitted_at'

@admin.register(ClaimAttachment)
class ClaimAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim', 'uploaded_at')
    search_fields = ('claim__employee__full_name',)


@admin.register(AssetInventory)
class AssetInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "asset_type",
        "serial_number",
        "purchased_date",
        "last_repaired_on",
        "is_active",
    )
    search_fields = ("asset_type", "serial_number")
    list_filter = ("asset_type", "is_active")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "inventory",
        "employee",
        "received_on",
        "returned_on",
        "is_with_employee",
    )
    list_filter = ("is_with_employee", "employee")
    search_fields = ("inventory__serial_number", "employee__full_name")

    def save_model(self, request, obj, form, change):
        if obj.returned_on:
            obj.is_with_employee = False
        super().save_model(request, obj, form, change)


