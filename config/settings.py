import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", default=0))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(' ')

# if "CSRF_TRUSTED_ORIGINS" in os.environ:
#     CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(' ')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "drf_yasg",

    # Custom apps
    "users",
    "directions.apps.DirectionsConfig",
    "main.apps.MainConfig",
]

CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    'http://10.4.134.142:5173',
    'http://192.168.64.1:5173',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost',
    'http://127.0.0.1', 
    'https://gxf7s1rd-5173.euw.devtunnels.ms',
]
CORS_ALLOW_HEADERS = ["Content-Type", "X-CSRFToken"]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://10.4.134.142:5173',
    'http://192.168.64.1:5173',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost',
    'http://127.0.0.1',
    'https://gxf7s1rd-5173.euw.devtunnels.ms'
]

# CSRF_COOKIE_SAMESITE = "None"
# SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
SESSION_COOKIE_HTTPONLY = True

# PROD ONLY
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # "DIRS": [os.path.join(BASE_DIR, 'build')],
        # "DIRS": [BASE_DIR / 'build'],
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("POSTGRES_DB", "db.sqlite3"),
        "USER": os.getenv("POSTGRES_USER", "user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTH_USER_MODEL = 'users.User'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'build/static')
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(seconds=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "UPDATE_LAST_LOGIN": False,

#     "ALGORITHM": "HS256",
#     "SIGNING_KEY": os.getenv("SECRET_KEY"),

#     "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",

#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
# }