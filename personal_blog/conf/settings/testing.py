from .base import *

PASSWORD_HASHERS = "django.contrib.auth.hashers.MD5PasswordHasher"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

DEBUG = False
