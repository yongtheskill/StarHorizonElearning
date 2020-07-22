"""
WSGI config for StarHorizonElearning project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/opt/bitnami/apps/django/django_projects/StarHorizonElearning')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/StarHorizonElearning/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StarHorizonElearning.settings")
from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()


import time
import traceback
import signal

try:
    application = get_wsgi_application()
    print ('WSGI without exception')
except Exception:
    print ('handling WSGI exception')
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)