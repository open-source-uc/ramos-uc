import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = os.getenv("SECRET_KEY", "VeryDifficultButDefaultSecret")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
if os.getenv("HOSTNAME"):
    ALLOWED_HOSTS += [os.getenv("HOSTNAME")]

if DEBUG and os.getenv("HOST_IP"):
    ALLOWED_HOSTS += [os.getenv("HOST_IP")]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "rest_framework",
    "manifest_loader",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "background_task",
    "apps.users.apps.UsersConfig",
    "apps.courses.apps.CoursesConfig",
    "apps.google_analytics.apps.GAConfig",
    "apps.courses_calification.apps.CoursesCalificationConfig",
    "apps.comments.apps.CommentsConfig",
    "apps.bc_scraper.apps.BCScraperConfig",
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

ROOT_URLCONF = "ramosuc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "front" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.google_analytics.context_processors.ga_code",
            ],
        },
    },
]

WSGI_APPLICATION = "ramosuc.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PSQL_DB", "django"),
        "USER": os.getenv("PSQL_USER", "postgres"),
        "PASSWORD": os.getenv("PSQL_PASSWD", "postgres"),
        "HOST": os.getenv("PSQL_HOST", "localhost"),
        "PORT": os.getenv("PSQL_PORT", ""),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
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


# Internationalization
LANGUAGE_CODE = "es-cl"
TIME_ZONE = os.getenv("TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static and media files
STATIC_URL = "/dist/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "front" / "static",
    BASE_DIR / "front" / "assets" / "dist",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Sites/Flatpages
SITE_ID = 1


# Base Authentication
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/cuentas/google/login"
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/")

# AllAuth
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.UCSocialAccountAdapter"

SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_ADAPTER = "apps.users.adapters.UCAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {}
if os.getenv("GOOGLE_AUTH_CLIENT") is not None:
    SOCIALACCOUNT_PROVIDERS["google"] = {
        "APP": {
            "client_id": os.getenv("GOOGLE_AUTH_CLIENT"),
            "secret": os.getenv("GOOGLE_AUTH_SECRET"),
            "key": "",
        }
    }


# Google analytics
GA_CODE = os.getenv("GA_CODE", None)

# BC-Scraper
SCRAPE_LOG = BASE_DIR / "logs" / "scrape.log"
SCRAPE_BATCH_SIZE = 100


# Cache
if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": BASE_DIR / "cache",
            "OPTIONS": {"MAX_ENTRIES": 800},
        }
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/django.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "WARNING"),
        },
    },
}
