import os
import platform
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Todo: Change secret key in production
SECRET_KEY = config("SECRET_KEY")

# Todo: Change to False in production
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis", 
    "accounts.apps.AccountsConfig",
    "vendor.apps.VendorConfig",
    "menu.apps.MenuConfig",
    "marketplace.apps.MarketplaceConfig",
    "django.contrib.postgres",
    "django_countries",
    "phonenumber_field",
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

ROOT_URLCONF = "earneats.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.get_vendor",
            ],
        },
    },
]

WSGI_APPLICATION = "earneats.wsgi.application"


# Database

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",  
        "ENGINE": "django.contrib.gis.db.backends.postgis",  # Use PostGIS engine for GeoDjango
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
    }
}

AUTH_USER_MODEL = "accounts.User"

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR /"static"
STATICFILES_DIRS = [
    "earneats/static"
]

# MEDIA FILES CONFUGURATIONS

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR /"media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# GOOGLE API CONFIGURATION
GOOGLE_API_KEY = config("GOOGLE_API_KEY")

# LOGGING CONFIGURATION
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'earneats': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# GEODJANGO CONFIGURATION

# Dynamic library path detection
if platform.system() == 'Darwin':  # macOS
    # Check for Homebrew installation (Apple Silicon)
    if os.path.exists('/opt/homebrew/lib'):
        GDAL_LIBRARY_PATH = '/opt/homebrew/lib/libgdal.dylib'
        GEOS_LIBRARY_PATH = '/opt/homebrew/lib/libgeos_c.dylib'
    # Check for Homebrew installation (Intel)
    elif os.path.exists('/usr/local/lib'):
        GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.dylib'
        GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.dylib'
elif platform.system() == 'Linux':
    # Common Linux paths
    GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
    GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so'