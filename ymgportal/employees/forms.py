from django import forms
from .models import Employee, MainClient, EndClient,LeaveApplication, MigrantType, Manager, PublicHoliday
from employees.business_logic.leave_service import working_days_between


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_serial_id',
            'full_name',
            'date_of_birth',
            'email',
            'phone',
            'main_account',
            'end_client',
            'client_account_manager',  # ✅ added
            'role_sow',
            'work_role',              # ✅ added
            'pass_type',
            'date_of_joining',
            'sow_start_date',
            'sow_end_date',
            'is_active',
            'is_pmo',
            'ph_allowed',
            'ot_allowed',
            'shift_hours_day',
            'shift_days_week',
            'yearly_annual_leave_entitlement',
            'yearly_sick_leave_entitlement',
            'location'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'sow_start_date': forms.DateInput(attrs={'type': 'date'}),
            'sow_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active managers
        self.fields['client_account_manager'].queryset = Manager.objects.filter(is_active=True)
        self.fields['client_account_manager'].label = "Client Account Manager"
        # Sort RoleSOW alphabetically
        self.fields['role_sow'].queryset = RoleSow.objects.all().order_by('name')
        self.fields['role_sow'].label = "Role / SOW"

class MainClientForm(forms.ModelForm):
    class Meta:
        model = MainClient
        fields = ['name']

class EndClientForm(forms.ModelForm):
    class Meta:
        model = EndClient
        fields = ['name', 'main_client']

class MigrantTypeForm(forms.ModelForm):
    class Meta:
        model = MigrantType
        fields = ['migrant_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['phone']  # Allow only email and phone to be edited
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }


from django import forms
from .models import RoleSow, Task

class RoleSowForm(forms.ModelForm):
    class Meta:
        model = RoleSow
        fields = ['name', 'description', 'main_client']

    def __init__(self, *args, **kwargs):
        super(RoleSowForm, self).__init__(*args, **kwargs)
        self.fields['main_client'].label = "Main Client"

from django import forms
from .models import TaskType, Task

class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task type name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task type description'}),
        }




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description'}),
            'type': forms.Select(attrs={'class': 'form-control'}),  # TaskType dropdown
        }

    def __init__(self, *args, **kwargs):
        rolesow = kwargs.pop('rolesow', None)  # Pop the RoleSow instance from the kwargs
        super(TaskForm, self).__init__(*args, **kwargs)
        if rolesow:
            # Filter the 'type' field to only include TaskTypes linked to the specified RoleSow
            self.fields['type'].queryset = TaskType.objects.filter(role_sow=rolesow)



# employees/forms.py
from django import forms
from .models import LeaveAdjustment

class LeaveAdjustmentForm(forms.ModelForm):
    class Meta:
        model = LeaveAdjustment
        fields = ["adjustment_type", "days", "reason"]

        widgets = {
            "adjustment_type": forms.Select(attrs={
                "class": "form-control",
                "style": "width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db;"
            }),
            "days": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.5",
                "style": "width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db;"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "style": "width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db;"
            }),
        }

from .models import Claim, ClaimAttachment

from django import forms
from .models import Claim, ClaimAttachment

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ["start_date", "end_date", "description", "amount"]

        widgets = {
            "start_date": forms.DateInput(attrs={
                "class": "input",
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "class": "input",
                "type": "date"
            }),
            "description": forms.Textarea(attrs={
                "class": "input",
                "rows": 3
            }),
            "amount": forms.NumberInput(attrs={
                "class": "input",
                "step": "0.01"
            }),
        }

class ClaimAttachmentForm(forms.Form):
    file = forms.FileField(required=True)


class PublicHolidayForm(forms.ModelForm):
    class Meta:
        model = PublicHoliday
        fields = ["holiday_name", "holiday_date", "country", "description", "is_active"]

        widgets = {
            "holiday_name": forms.TextInput(attrs={"class": "form-input"}),
            "holiday_date": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "country": forms.Select(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
        }



# employees/forms.py

class LeaveApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop("employee", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        leave_type = cleaned.get("leave_type")

        if not start_date or not end_date:
            return cleaned

        if start_date > end_date:
            raise forms.ValidationError("End date cannot be before start date.")

        # Leave days are counted on weekdays only (Mon-Fri).
        # Weekend-only selections are not valid leave applications.
        working_days = working_days_between(start_date, end_date)
        is_half_day = bool(
            leave_type and leave_type.name and "half" in leave_type.name.lower()
        )
        if working_days == 0:
            raise forms.ValidationError(
                "Selected range has no working days (Mon-Fri). Please choose a working day."
            )
        if is_half_day and working_days > 1:
            raise forms.ValidationError(
                "Half-day leave can be applied only for a single working day."
            )

        if self.employee:
            qs = LeaveApplication.objects.filter(employee=self.employee).exclude(status="REJECTED")
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            overlaps = qs.filter(start_date__lte=end_date, end_date__gte=start_date)
            if overlaps.exists():
                raise forms.ValidationError(
                    "You already have a leave application overlapping these dates. "
                    "Please pick different dates."
                )

        return cleaned

    class Meta:
        model = LeaveApplication
        fields = ["leave_type", "start_date", "end_date", "reason"]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }
