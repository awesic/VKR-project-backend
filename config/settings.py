import os
from pathlib import Path
from secrets import token_hex
from django.conf.global_settings import LANGUAGES as DJANGO_LANGUAGES

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", token_hex(32))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(' ')

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    
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

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_EXPOSE_HEADERS = os.environ.get("CORS_EXPOSE_HEADERS").split(' ')
# CORS_ALLOW_HEADERS = os.environ.get("CORS_ALLOW_HEADERS").split(' ')
CORS_ALLOW_CREDENTIALS = os.environ.get("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", 'http://localhost http://127.0.0.1:8000').split(' ')
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost http://127.0.0.1:8000').split(' ')
SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN', '127.0.0.1')
CSRF_COOKIE_DOMAIN = os.environ.get('CSRF_COOKIE_DOMAIN', 'localhost')
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

if os.environ.get("PRODUCTION", 'False').lower() == "true":
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = False

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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

# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("ENGINE", "django.db.backends.sqlite3"),
#         "NAME": os.environ.get("POSTGRES_DB", "db.sqlite3"),
#         "USER": os.environ.get("POSTGRES_USER", "user"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
#         "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
#         "PORT": os.environ.get("POSTGRES_PORT", "5432"),
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
USE_I18N = True
USE_L10N = True
USE_TZ = True
# English default
LANGUAGES = DJANGO_LANGUAGES


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

JAZZMIN_SETTINGS = {
    "site_title": "VKR-tracker admin-site",
    "welcome_sign": "Вход в админку",
    "site_header": "Админка",
    "site_brand": "Adminka",
    "site_logo": "img/logo_color.png",
    "site_logo_classes": "img-circle",
    "copyright": "VKR-tracker",
    
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": ["users.User", "users.Teacher", "users.Student"],
    # Add a language dropdown into the admin
    # "language_chooser": True,
    "order_with_respect_to": ["main", "users", "users.User", "users.Teacher", "users.Student"],
    
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "users": [{
            "name": "Подтвердить науч рука", 
            "url": "http://127.0.0.1:8000/api/v1/students", 
            "icon": "fas fa-comments",
            "permissions": ["users.view_users"]
        }]
    },
    
    "icons": {
        "users": "fas fa-users-cog",
        "users.User": "fas fa-user",
        "users.Teacher": "fas fa-user-tie",
        "users.Student": "fas fa-user-graduate",
        
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    # "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}