import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

sentry_logging = LoggingIntegration(
    level=logging.WARNING, event_level=logging.WARNING
)

sentry_sdk.init(
    dsn=get_secret("DSN_SENTRY"),
    integrations=[DjangoIntegration(), sentry_logging],
    server_name="ubuntu_eu_central",
)
