#!/bin/sh

# Reference: https://testdriven.io/courses/tdd-django/postgres-setup/

: '
The script is used to wait for the PostgreSQL database to be available, flush and migrate the database
and then execute the command to start the Django application server.
Common practice to include scripts like this in Docker containers to perform initialisation tasks
before running the main application.
'

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while !nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"