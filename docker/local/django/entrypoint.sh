#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python << END
import sys
import time
import psycopg2

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        psycopg2.connect(
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for database connection...\n")
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("Unable to connect to the database. Error: " + str(error) + "\n")
            sys.exit(1)
        time.sleep(1)

END

>&2 echo "Connected to database"

exec "$@"