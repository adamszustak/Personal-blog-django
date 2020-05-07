import os
import json

from django.core.exceptions import ImproperlyConfigured

with open("conf/settings/config.json") as config_file:
    secrets = json.load(config_file)


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "comments.apps.CommentsConfig",
    "ckeditor",
    "ckeditor_uploader",
    "crispy_forms",
    "google_analytics",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.list_all",
                "blog.context_processors.list_category",
            ],
        },
    },
]

WSGI_APPLICATION = "conf.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "personal_blog",
        "USER": get_secret("NAME_DB"),
        "PASSWORD": get_secret("PASS_DB"),
        "HOST": "localhost",
        "PORT": "",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DEFAULTUSERMAIL = "madasz@onet.eu"

CRISPY_TEMPLATE_PACK = "bootstrap4"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        "toolbar_Full": [
            [
                "Styles",
                "CodeSnippet",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["NumberedList", "BulletedList"],
            ["Indent", "Outdent"],
            ["Maximize"],
        ],
        "codeSnippet_languages": {
            "python": "Python",
            "sql": "SQL",
            "json": "JSON",
        },
        "extraPlugins": "justify,liststyle,indent,codesnippet",
    },
}

CKEDITOR_UPLOAD_PATH = "post_upload/"
CKEDITOR_ALLOW_NONIMAGE_FILES = False

GOOGLE_ANALYTICS = {
    "google_analytics_id": get_secret("GOOGLE_ID"),
}


BLOG_TITLE = "UczsieIT!"
BLOG_DESCRIPTION = "Blog zawierający artykuły na temat Pythona i Django. Jeśli chcesz poznać praktyczne oblicze Pythona to koniecznie sprawdź!"
KEYWORDS = "Ucz sie IT, Informatyka, Informatics, Nauka, Science, Komputery, Computers, Python, Django"