import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import MainClient, RoleSow, Employee


class Command(BaseCommand):
    """
    Seeds the CI/CD database with the minimum data that Playwright tests
    depend on. Safe to run on every build — all operations are idempotent.

    Env vars consumed (all injected by Jenkins withCredentials):
        TEST_ADMIN_USER / TEST_ADMIN_PASS    — admin superuser
        TEST_EMPLOYEE_USER / TEST_EMPLOYEE_PASS — employee portal user
    """
    help = 'Seeds CI database with data required for Playwright tests'

    def handle(self, *args, **kwargs):
        self._seed_superuser()
        self._seed_main_client()
        self._seed_role_sow()
        self._seed_employee_user()
        self.stdout.write(self.style.SUCCESS('CI seed complete.'))

    # ------------------------------------------------------------------
    def _seed_superuser(self):
        username = os.environ.get('TEST_ADMIN_USER', 'admin')
        password = os.environ.get('TEST_ADMIN_PASS', 'changeme')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': 'admin@ci.test', 'is_staff': True, 'is_superuser': True},
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=['password', 'is_staff', 'is_superuser'])

        label = 'Created' if created else 'Updated'
        self.stdout.write(f'{label} superuser: {username}')

    def _seed_main_client(self):
        client, created = MainClient.objects.get_or_create(name='Robert')
        if created:
            self.stdout.write(self.style.SUCCESS('Created MainClient: Robert'))

    def _seed_role_sow(self):
        client = MainClient.objects.get(name='Robert')
        role, created = RoleSow.objects.get_or_create(
            name='johndoe',
            defaults={'description': 'CI seed data', 'main_client': client},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created RoleSow: johndoe'))

    def _seed_employee_user(self):
        """
        Creates a regular Django user + linked Employee record for the
        employee-portal Playwright tests.  Skipped silently if
        TEST_EMPLOYEE_USER is not set (admin-only test runs).
        """
        username = os.environ.get('TEST_EMPLOYEE_USER')
        password = os.environ.get('TEST_EMPLOYEE_PASS')

        if not username or not password:
            self.stdout.write('TEST_EMPLOYEE_USER not set — skipping employee seed.')
            return

        client = MainClient.objects.get(name='Robert')

        user, u_created = User.objects.get_or_create(
            username=username,
            defaults={'email': username if '@' in username else f'{username}@ci.test'},
        )
        user.set_password(password)
        user.save(update_fields=['password'])

        emp, e_created = Employee.objects.get_or_create(
            user=user,
            defaults={
                'full_name': 'CI Employee',
                'email': user.email,
                'main_account': client,
            },
        )

        label = 'Created' if u_created else 'Updated'
        self.stdout.write(f'{label} employee user: {username}')
