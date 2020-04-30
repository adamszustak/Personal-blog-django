from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES["default"].update(
    {"PORT": "5432",}
)
