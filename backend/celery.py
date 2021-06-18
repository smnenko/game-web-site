import os

from celery import Celery
from celery.schedules import crontab

from django.core import management

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

#  sudo rabbitmq-server
#  celery -A backend beat -l info
#  celery -A backend worker -l INFO


@app.task(bind=True)
def load_games_from_igdb():
    management.call_command('load_games')


app.conf.beat_schedule = {
    "load games from igdb database": {
        'task': 'backend.celery.load_games_from_igdb',
        'schedule': crontab(hour='6, 18'),
    }
}
