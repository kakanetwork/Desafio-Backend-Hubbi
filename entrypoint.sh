#!/bin/sh

# Espera o Postgres e Redis para poder iniciar os demais (são serviços essenciais)
echo "Esperando pelo PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Esperando pelo Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 1
done

# Aplica migrations
echo "Aplicando migrations..."
python manage.py migrate --noinput

# Se o comando tiver sido passado, executa abaixo
if [ "$1" = "celery_worker" ]; then
    echo "Iniciando Celery Worker..."
    celery -A marketplace worker -l info
elif [ "$1" = "celery_beat" ]; then
    echo "Iniciando Celery Beat..."
    celery -A marketplace beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
    # Comando default: Django
    echo "Iniciando Django..."
    python manage.py runserver 0.0.0.0:8000
fi

# Executa o comando passado para o container (de iniciar o Django, Celery, etc)
exec "$@"
