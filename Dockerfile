FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code
COPY . /code/

RUN apt-get update &&apt-get install python3-dev libpq-dev -y
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

RUN pipenv run ./manage.py collectstatic --noinput
