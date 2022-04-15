import os

from celery import Celery, shared_task

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
    management.call_command('load_games')
