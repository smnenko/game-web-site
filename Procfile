web: pipenv run ./manage.py collectstatic --noinput && wait && pipenv run ./manage.py compilescss && wait && pipenv run ./manage.py migrate && wait && pipenv run ./manage.py loaddata initial.json && wait && pipenv run gunicorn backend.wsgi:application --preload --log-file -
beat: celery -A backend beat -l INFO
worker: celery -A backend worker -l INFO