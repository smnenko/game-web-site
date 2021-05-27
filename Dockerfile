FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
COPY . /code/