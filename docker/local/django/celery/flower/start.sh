#!/bin/bash

set -o errexit

set -o nounset

worker_ready(){
    celery -A estatemgm.celery_app inspect ping
}

until worker_ready; do 
    >&2 echo 'Celery workers not available :-('
    sleep 1

done
>&2 echo 'Celery workers are available and ready!...:-)'

# exec watchfiles --filter python celery.__main__.main --args '-A estatemgm.config.celery_app -b \"${CELERY_BROKER_URL}\" flower --basic-auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\"'
celery --app=estatemgm.celery_app --broker="${CELERY_BROKER_URL}" flower