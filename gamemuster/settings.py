import os
import sys
from pathlib import Path

import environ
from celery.schedules import crontab

PROJECT_DIR = Path(__file__).parent
BASE_DIR = PROJECT_DIR.parent
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

env = environ.Env()
environ.Env.read_env(open(BASE_DIR.joinpath('.env')))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split()

IGDB_CLIENT_ID = env('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = env('IGDB_CLIENT_SECRET')

TWITTER_KEY = env('TWITTER_KEY')
TWITTER_SECRET = env('TWITTER_SECRET')
TWITTER_BEARER = env('TWITTER_BEARER')

THIRD_PARTY_APPS = [
    'imagekit',
    'debug_toolbar',
    'sass_processor',
    'corsheaders'
]

PROJECT_APPS = [
    'core',
    'game',
    'user'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *PROJECT_APPS
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gamemuster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'gamemuster.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

REDIS_URL = (
    f"redis://{env('REDIS_USER')}:{env('REDIS_PASS')}@"
    f"{env('REDIS_HOST')}:{env('REDIS_PORT')}/"
    f"{env('REDIS_NAME')}"
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL
    }
}

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

CORS_ALLOWED_ORIGINS = [f'https://{i}' for i in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [PROJECT_DIR.joinpath('static')]

STATIC_ROOT = BASE_DIR.joinpath('deploy').joinpath('static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('deploy').joinpath('media')

CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = REDIS_URL
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULE = {
    'test_task': {
        'task': 'gamemuster.celery.test_task',
        'schedule': crontab(minute='*')
    },
    'load_games_from_igdb': {
        'task': 'gamemuster.celery.load_games_from_igdb',
        'schedule': crontab(hour='6, 18')
    }
}

AUTH_USER_MODEL = 'user.CustomUser'
LOGIN_URL = '/user/login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]
