from os import getenv, path
from dotenv import load_dotenv
from .base import *

local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(dotenv_path=local_env_file)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_NAME = getenv('SITE_NAME', 'Estates Management')
SECRET_KEY =  getenv('DJANGO_SECRET_KEY', 'django-insecure--_25sa8yzt8ktulcc+sbuo91)z7v)_vnv1x#=imsq-2kqb!ua=')

ADMIN_URL = getenv('DJANGO_ADMIN_URL', 'admin')
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT =  int(getenv('EMAIL_PORT', 25))
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
DOMAIN = getenv('DOMAIN', 'localhost')


# Define loggers

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            "format": '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}