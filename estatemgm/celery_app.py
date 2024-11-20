import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estatemgm.settings.local')

app = Celery('estatemgm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
#Dong nay co nghia la celery se tu tim kiem cac task trong cac app.
# Cac task trong app duoc viet tai tasks.py