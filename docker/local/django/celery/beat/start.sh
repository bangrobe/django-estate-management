#!/bin/bash

set -o errexit

set -o nounset

rm -rf './celerybeat.pid'

exec watchfiles --filter python celery.__main__.main --args '-A estatemgm.celery_app beat -l info'