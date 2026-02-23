from .settings import *

# use temporary DB for Jenkins tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'jenkins_test_db.sqlite3',
    }
}

# faster password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

DEBUG = True
ALLOWED_HOSTS = ['*']