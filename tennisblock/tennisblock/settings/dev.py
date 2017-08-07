print ("Running Development Settings.")
import environ

env = environ.Env()

env("RAVEN_CONFIG", default='https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@sentry.io/29740')

from .base import *

DEBUG = True

# Set this for development, but clear for PROD
BLOCK_NOTIFY_RECIPIENTS = ['ed@tennisblock.com', 'viquee@me.com']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

FIXTURE_DIRS = (
    PROJECT_ROOT.child('fixtures'),
)

