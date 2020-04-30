from django.contrib.auth.models import User

from django.conf import settings


def get_default_user():
    return User.objects.get(email=settings.DEFAULTUSERMAIL)
