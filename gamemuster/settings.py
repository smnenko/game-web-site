import os
import sys
from pathlib import Path

from celery.schedules import crontab

PROJECT_DIR = Path(__file__).parent
BASE_DIR = PROJECT_DIR.parent
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

DEVELOPMENT = 'DEVELOPMENT'
PRODUCTION = 'PRODUCTION'
ENVIRONMENT = DEVELOPMENT if os.path.exists(BASE_DIR.joinpath('.env')) else PRODUCTION

if ENVIRONMENT == DEVELOPMENT:
    from dotenv import load_dotenv
    load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = bool(int(os.environ.get('DEBUG', 1)))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

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
    'django.contrib.admindocs',
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
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASS'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT')
    }
}

REDIS_NAME = os.environ.get('REDIS_NAME')
REDIS_USER = os.environ.get('REDIS_USER')
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

REDIS_URL = (
    f"redis://{REDIS_USER}:{REDIS_PASS}@"
    f"{REDIS_HOST}:{REDIS_PORT}/"
    f"{REDIS_NAME}"
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

IGDB_CLIENT_ID = os.environ.get('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.environ.get('IGDB_CLIENT_SECRET')

TWITTER_KEY = os.environ.get('TWITTER_KEY')
TWITTER_SECRET = os.environ.get('TWITTER_SECRET')
TWITTER_BEARER = os.environ.get('TWITTER_BEARER')
