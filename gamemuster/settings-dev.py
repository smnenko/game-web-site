import environ

from .settings import *


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

REDIS_NAME = env('REDIS_NAME')
REDIS_USER = env('REDIS_USER')
REDIS_PASS = env('REDIS_PASS')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT')
    }
}
