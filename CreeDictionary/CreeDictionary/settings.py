"""
Django settings for CreeDictionary project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import logging
import os
import posixpath
from pathlib import Path
from sys import stderr

from .hostutils import HOST_IS_SAPIR, HOSTNAME

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "72bcb9a0-d71c-4d51-8694-6bbec435ab34"

# sapir.artsrn.ualberta.ca has some... special requirements,
# so let's hear about it!
RUNNING_ON_SAPIR = (
    os.environ.get("RUNNING_ON_SAPIR", str(HOST_IS_SAPIR)).lower() == "true"
)

# Debug is default to False
# Turn it to True in development
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# SECURITY WARNING: don't run with debug turned on in production!
if RUNNING_ON_SAPIR:  # pragma: no cover
    assert not DEBUG

# travis has CI equals True
CI = os.environ.get("CI", "False").lower() == "true"

if DEBUG:
    ALLOWED_HOSTS = ["*"]
elif RUNNING_ON_SAPIR:  # pragma: no cover
    ALLOWED_HOSTS = ["sapir.artsrn.ualberta.ca"]
else:  # pragma: no cover
    ALLOWED_HOSTS = [HOSTNAME]

# Application definition

INSTALLED_APPS = [
    # Add your apps here to enable them
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "API.apps.APIConfig",
    "CreeDictionary.apps.CreeDictionaryConfig",
    "morphodict.apps.MorphodictConfig",
    "django_js_reverse",
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

# configure tools for development, CI, and production
if DEBUG:
    if not CI:  # enable django-debug-toolbar for development
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(
            0, "debug_toolbar.middleware.DebugToolbarMiddleware"
        )  # middleware order is important

        # works with django-debug-toolbar app
        DEBUG_TOOLBAR_CONFIG = {
            # Toolbar options
            "SHOW_COLLAPSED": True,  # collapse the toolbar by default
        }

        INTERNAL_IPS = ["127.0.0.1"]

if RUNNING_ON_SAPIR:  # pragma: no cover
    # Sapir uses `wsgi_express` that requires mod_wsgi
    INSTALLED_APPS.append("mod_wsgi.server")

ROOT_URLCONF = "CreeDictionary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # 'threaded': True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "CreeDictionary.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

USE_TEST_DB = os.environ.get("USE_TEST_DB", "False").lower() == "true"
# if this is set, then use existing test database


if not USE_TEST_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        }
    }
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

############################### Morphodict configuration ###############################

# Configure the orthographies
MORPHODICT_ORTHOGRAPHY = {
    # 'Latn' is Okimāsis/Wolvegrey's SRO
    "default": "Latn",
    "available": {
        "Latn": {"name": "SRO (êîôâ)"},
        "Latn-x-macron": {"name": "SRO (ēīōā)"},
        "Cans": {"name": "Syllabics"},
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

############################## API app settings ###############################

# We only apply affix search for user queries longer than the threshold length
AFFIX_SEARCH_THRESHOLD = 4

############################## staticfiles app ###############################

if RUNNING_ON_SAPIR:  # pragma: no cover
    # on sapir /cree-dictionary/ is used to identify the service of the app
    # XXX: this is kind of a hack :/
    STATIC_URL = "/cree-dictionary/static/"
else:
    STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

if DEBUG:
    # Use the default static storage backed for debug purposes.
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    # In production, use a manifest to encourage aggressive caching
    # Note requires `python manage.py collectstatic`!
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

log_dir = Path(BASE_DIR) / "django_logs"
log_dir.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "require_run_main_true": {"()": "CreeDictionary.settings.RunMainFilter"},
    },
    "handlers": {
        "write_debug_to_file_prod": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / "django.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "filters": ["require_debug_false"],
        },
        "write_info_to_console_dev": {
            "level": "INFO",
            # without require_run_main_true, loggers from API.apps will print twice
            "filters": ["require_debug_true", "require_run_main_true"],
            "class": "logging.StreamHandler",
        },
    },  # learn how different loggers are used in django: https://docs.djangoproject.com/en/3.0/topics/logging/#id3
    "loggers": {
        "django": {
            "handlers": ["write_debug_to_file_prod", "write_info_to_console_dev"],
            "level": "DEBUG",
        },
        # loggers created with logging.get_logger(__name__) under API app will use the configuration here
        "API": {
            "handlers": ["write_debug_to_file_prod", "write_info_to_console_dev"],
            "level": "DEBUG",
        },
    },
}


class RunMainFilter(logging.Filter):
    """
    When DEBUG is True, django clones two processes, one is the main processes, while the other is for hot swapping.
    The main process sets RUN_MAIN to true
    """

    def filter(self, record):
        return os.environ.get("RUN_MAIN") == "true"
