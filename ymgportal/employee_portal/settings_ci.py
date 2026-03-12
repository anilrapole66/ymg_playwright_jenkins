from .settings import *
import os

# Override SECRET_KEY for CI
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-ci-only-key-not-for-production-use')

# CI database (temporary SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ci_test_db.sqlite3',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

DEBUG = True
ALLOWED_HOSTS = ['*']