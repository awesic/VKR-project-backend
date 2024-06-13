#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PGHOST $PGPORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
# python manage.py makemigrations
# python manage.py migrate

# python manage.py import_institutes
# echo "Institutes imported"

# python manage.py import_directions
# echo "Directions imported"

# python manage.py import_departments
# echo "Departments imported"

python manage.py collectstatic --no-input

cp -r static/* django-static/
# gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

exec "$@"