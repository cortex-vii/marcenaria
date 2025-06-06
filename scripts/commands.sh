#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Espere for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Iniciou Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"
pip install -r requirements.txt && \
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "✅ Creating superuser 'root'..."
export DJANGO_SUPERUSER_USERNAME=root
export DJANGO_SUPERUSER_EMAIL=root@example.com 
export DJANGO_SUPERUSER_PASSWORD=231212
python manage.py createsuperuser --noinput || echo "Superuser 'root' already exists or an error occurred during creation."


python manage.py runserver 0.0.0.0:8000 --verbosity 3

