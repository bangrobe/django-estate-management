#!/bin/bash

set -o errexit

set -o nounset

exec watchfiles --filter python celery.__main__.main --args '-A estatemgm.celery_app worker --loglevel=info'