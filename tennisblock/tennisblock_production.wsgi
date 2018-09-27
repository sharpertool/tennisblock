import os
import sys
from path import path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_ROOT = os.path.abspath(os.path.join(BASE_DIR, '.'))

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock_dj.settings.production")

import tennisblock_dj.monitor
tennisblock_dj.monitor.start(interval=1.0)
tennisblock_dj.monitor.track(os.path.join(os.path.dirname(__file__), 'tennisblock_production.wsgi'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
