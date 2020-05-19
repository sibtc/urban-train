import os
import environ

BASE_DIR = environ.Path(__file__) - 2
ROOT_DIR = environ.Path(__file__) - 2

env = environ.Env()
env.read_env(ROOT_DIR('.envs/.local/.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY', default='apjfqc9e8r-9eq3r3u49u4399r43-@#%^^^')

APPS_DIR = ROOT_DIR.path("urban-train")

DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = [
    'gastosluxu.com.br',
    'localhost',
    '127.0.0.1',
    '172.105.148.155',
    'gastosluxu.herokuapp.com'
]

INSTALLED_APPS = [
    # General use templates & template tags (should appear first)
    'django_adminlte',
    # Optional: Django admin theme (must be before django.contrib.admin)
    # 'django_adminlte_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # lib
    'debug_toolbar',
    'widget_tweaks',
    'django_extensions',
    'django_select2',
    'django_ajax',
    # "django_summernote",
    # Third-party
    'crispy_forms',
    'dynamic_formsets',
    'cruds_adminlte',
    'table',
    # apps
    # 'core',
    'accounts',
    'website'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'urban_train.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'urban_train.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# postgres://USER:PASSWORD@HOST:PORT/NAME
# DATABASES = {
#     'default': env.db('DATABASE_URL', default='postgres:///promosys'),
# }
# DATABASES['default']['ATOMIC_REQUESTS'] = True
# DATABASES['default']['conn_max_age'] = 600

# If use POSTGRES and AWS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# STATIC
STATIC_URL = "/static/"
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/django-summernote/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# auth
LOGIN_URL = '/entrar/'
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.ModelBackend',
)

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# MEDIA_URL = "/django-summernote/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

SUMMERNOTE_CONFIG = {
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,
        'lang': 'pt-BR',
    }
}
