print ("Running Development Settings.")
import environ

env = environ.Env()

env("RAVEN_CONFIG", default='https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@sentry.io/29740')

from .base import *

DEBUG = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

FIXTURE_DIRS = (
    PROJECT_ROOT('fixtures'),
)

INSTALLED_APPS += (
    'django_extensions',
)

