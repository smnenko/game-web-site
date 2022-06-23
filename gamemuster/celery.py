import os

from celery import Celery
from django.core.cache import cache

from django.core import management


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamemuster.settings')

app = Celery('gamemuster')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#  sudo rabbitmq-server
#  celery -A gamemuster beat -l info
#  celery -A gamemuster worker -l INFO


@app.task(bind=True)
def test_task(self):
    print('Test task is executed')


@app.task(bind=True)
def load_games_from_igdb(self):
    cache_name = 'load_games_offset'
    if cache.get(cache_name):
        offset = cache.get(cache_name)
        management.call_command(f'load_games', offset=offset)
        cache.set(cache_name, offset + 500, 60 * 60 * 24)
    else:
        management.call_command(f'load_games', offset=0)
        cache.set(cache_name, 500, 60 * 60 * 24)
