#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

from django.conf import settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamemuster.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if settings.ENVIRONMENT == settings.PRODUCTION and sys.argv[1] == 'runserver':
        subprocess.Popen(['celery', '-A', 'gamemuster', 'beat', '-l', 'INFO'])
        subprocess.Popen(['celery', '-A', 'gamemuster', 'worker', '-l', 'INFO'])

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
