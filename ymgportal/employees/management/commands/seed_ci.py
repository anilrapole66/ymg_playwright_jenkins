import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import MainClient, RoleSow


class Command(BaseCommand):
    """
    Seeds the CI/CD database with the minimum lookup data that Playwright
    tests depend on.  Safe to run on every build — all operations are
    idempotent (get_or_create / update).

    Usage:
        python manage.py seed_ci

    Credentials are read from env vars TEST_ADMIN_USER / TEST_ADMIN_PASS
    (injected by Jenkins from the PLAYWRIGHT_ADMIN credential).
    """
    help = 'Seeds CI database with data required for Playwright tests'

    def handle(self, *args, **kwargs):
        self._seed_superuser()
        self._seed_main_client()
        self._seed_role_sow()
        self.stdout.write(self.style.SUCCESS('CI seed complete.'))

    # ------------------------------------------------------------------
    def _seed_superuser(self):
        username = os.environ.get('TEST_ADMIN_USER', 'admin')
        password = os.environ.get('TEST_ADMIN_PASS', 'changeme')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': 'admin@ci.test', 'is_staff': True, 'is_superuser': True},
        )
        # Always sync the password so rotated Jenkins credentials take effect
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
