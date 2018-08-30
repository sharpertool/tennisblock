print ("Running Development Settings.")

from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    }
}

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@app.getsentry.com/29740',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

FIXTURE_DIRS = (
    PROJECT_ROOT.child('fixtures'),
)




