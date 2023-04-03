#!/bin/sh

set -ex

# Wait for the database container
# See: https://docs.docker.com/compose/startup-order/
export PGHOST=${DB_HOST:-db}
export PGPORT=${DB_PORT:-5432}

fixtures_dir=${FIXTURES_DIR:-/app/schools/fixtures}

uwsgi_port=${UWSGI_PORT:-8000}
uwsgi_processes=${UWSGI_PROCESSES:-2}
uwsgi_threads=${UWSGI_THREADS:-2}

mountpoint=${SUBPATH:-/}

until pg_isready; do
  >&2 echo "Waiting for database connection..."
  sleep 1
done

>&2 echo "Database is up."

# Apply database migrations
>&2 echo "Apply database migrations"
python src/manage.py migrate

# Load any JSON fixtures present
if [ -d $fixtures_dir ]; then
    echo "Loading fixtures from $fixtures_dir"

    for fixture in $(ls "$fixtures_dir/"*.json)
    do
        echo "Loading fixture $fixture"
        python src/manage.py loaddata $fixture
    done
fi

# Create superuser
# specify password by setting POLYTRIP_SUPERUSER_PASSWORD in the env
# specify username by setting POLYTRIP_SUPERUSER_USERNAME in the env
# specify email by setting POLYTRIP_SUPERUSER_EMAIL in the env
if [ -n "${POLYTRIP_SUPERUSER_USERNAME}" ]; then
    python src/manage.py createinitialsuperuser \
        --no-input \
        --username "${POLYTRIP_SUPERUSER_USERNAME}" \
        --email "${POLYTRIP_SUPERUSER_EMAIL:-admin@admin.org}"
    unset POLYTRIP_SUPERUSER_USERNAME POLYTRIP_SUPERUSER_EMAIL POLYTRIP_SUPERUSER_PASSWORD
fi

# Start server
>&2 echo "Starting server"
uwsgi \
    --http :$uwsgi_port \
    --http-keepalive \
    --manage-script-name \
    --mount $mountpoint=polytrip.wsgi:application \
    --static-map /static=/app/static \
    --static-map /media=/app/media \
    --chdir src \
    --enable-threads \
    --processes $uwsgi_processes \
    --threads $uwsgi_threads \
    --buffer-size=65535
