import environ

print("Running Development Settings.")

env = environ.Env()

env("RAVEN_CONFIG", default='https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@sentry.io/29740')

from .common import *

DEBUG = True

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

FIXTURE_DIRS = (
    PROJECT_ROOT('fixtures'),
)

INTERNAL_IPS = [
    '127.0.0.1',
    'tennisblock.local'
]