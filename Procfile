web: python3 manage.py collectstatic --noinput && wait && python3 manage.py compilescss && wait && python3 manage.py flush --noinput && wait && python3 manage.py migrate && wait && python3 manage.py loaddata initial.json && wait && python3 gunicorn gamemuster.wsgi:application --preload --log-file -
beat: celery -A backend beat -l INFO
worker: celery -A backend worker -l INFO