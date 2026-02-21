from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import upload_medical_certificate, delete_medical_certificate, list_medical_certificates

urlpatterns = [
    path('', views.user_redirect, name='user_redirect'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('employee_home/', views.employee_home, name='employee_home'),

    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
path("employee/<int:pk>/edit/", views.employee_edit, name="employee_edit"),
path('login/', auth_views.LoginView.as_view(
    template_name='employees/login.html',
    next_page='/'
), name='login'),


    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/'  # Redirect to login after logout
    ), name='logout'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('upload-employees/', views.upload_employees, name='upload_employees'),
    path('configurables/', views.configurables_view, name='configurables'),
    path('configurables/add-main-client/', views.add_main_client, name='add_main_client'),
    path('configurables/add-end-client/', views.add_end_client, name='add_end_client'),
    path('configurables/add-migrant-type/', views.add_migrant_type, name='add_migrant_type'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('configurables/roles/', views.configurables_roles, name='configurables_roles'),
    path('configurables/roles/<int:rolesow_id>/', views.configurables_role_details, name='configurables_role_details'),
    path('configurables/roles/add/', views.add_rolesow, name='add_rolesow'),
    path('configurables/roles/<int:rolesow_id>/add_task_type/', views.add_task_type, name='add_task_type'),
    path('configurables/roles/<int:rolesow_id>/add_task/', views.add_task, name='add_task'),
    path('submit_timesheet/', views.submit_timesheet, name='submit_timesheet'),
    path('saved_timesheets/', views.saved_timesheets, name='saved_timesheets'),
    path('export_timesheet/<int:submission_id>/', views.export_timesheet_file, name='export_timesheet_file'),
    path("admin_timesheets/", views.admin_timesheets, name="admin_timesheets"),
    path("export_timesheet/<int:employee_id>/<int:month>/<int:year>/",
     views.export_timesheet, name="export_timesheet"),
    path('export_multiple_timesheets/', views.export_multiple_timesheets, name='export_multiple_timesheets'),

path("upload_medical_certificate/", upload_medical_certificate, name="upload_medical_certificate"),
path("list_medical_certificates/", list_medical_certificates, name="list_medical_certificates"),
path("delete_medical_certificate/", delete_medical_certificate, name="delete_medical_certificate"),

path("employee/<int:pk>/leaves/", views.employee_leave_details, name="employee_leave_details"),
path("employee/<int:pk>/timesheets/", views.employee_timesheets, name="employee_timesheets"),
path("employee/<int:pk>/claims/", views.employee_claims, name="employee_claims"),
path("employee/<int:pk>/leave-adjustment/add/", views.leave_adjustment_add, name="leave_adjustment_add"),
path("claims/submit/", views.claim_submit, name="claim_submit"),
path("claims/", views.claim_list, name="claim_list"),
path("claims/<int:claim_id>/", views.claim_detail, name="claim_detail"),
path("admin_claims/", views.admin_claims, name="admin_claims"),
path("admin_claims/<int:claim_id>/", views.admin_claim_detail, name="admin_claim_detail"),
path("admin_claims/<int:claim_id>/reject/", views.admin_reject_claim, name="admin_reject_claim"),
path("active_dashboard/", views.active_user_dashboard, name="active_dashboard"),
path("timesheet/<int:submission_id>/approve/", views.approve_timesheet, name="approve_timesheet"),
path("timesheet/<int:submission_id>/reject/", views.reject_timesheet, name="reject_timesheet"),
path("public-holidays/", views.public_holidays, name="public_holidays"),
path("public-holidays/add/", views.add_public_holiday, name="add_public_holiday"),
path("public-holidays/edit/<int:pk>/", views.edit_public_holiday, name="edit_public_holiday"),
path("public-holidays/delete/<int:pk>/", views.delete_public_holiday, name="delete_public_holiday"),
# Manager dashboard routes
path("manager/employees/", views.manager_employee_list, name="manager_employee_list"),
path("manager/timesheets/", views.manager_timesheets, name="manager_timesheets"),
path("manager/leaves/", views.manager_leave_details, name="manager_leave_details"),
path("leave-history/", views.leave_history, name="leave_history"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
path(
    "employee/configure-tasks/",
    views.employee_configure_tasks,
    name="employee_configure_tasks"
),
path(
    "employee/add-task/",
    views.employee_add_task,
    name="employee_add_task"
),

path(
    "configurables/tasks/<int:task_id>/toggle-active/",
    views.toggle_task_active,
    name="toggle_task_active"
),
path(
    "employee/assets/",
    views.employee_assets,
    name="employee_assets"
),

path(
    "assets/",
    views.admin_assets,
    name="admin_assets"
),

path("assets/inventory/", views.admin_inventory, name="admin_inventory"),
path("assets/assign/", views.assign_asset, name="assign_asset"),
path(
    "assets/inventory/add/",
    views.add_inventory,
    name="add_inventory"
),
path("assets/inventory/<int:inventory_id>/edit/", views.edit_inventory, name="edit_inventory"),
path(
    "assets/assignment/<int:asset_id>/edit/",
    views.edit_assignment,
    name="edit_assignment"
),
path("leave-apply/", views.apply_leave, name="apply_leave"),
# Leave approvals (Admin)
path(
    "leaves/approvals/",
    views.admin_leave_approvals,
    name="admin_leave_approvals"
),

path(
    "leaves/<int:leave_id>/approve/",
    views.approve_leave,
    name="approve_leave"
),

path(
    "leaves/<int:leave_id>/reject/",
    views.reject_leave,
    name="reject_leave"
),


]
