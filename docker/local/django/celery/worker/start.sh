#!/bin/bash

set -o errexit

set -o nounset

exec watchfiles --filter python celery.__main__.main --args '-A estatemgm.config.celery worker --loglevel=info'