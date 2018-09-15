import environ
import sys

print("Loaded local_config from %s." % __file__)

env = environ.Env()

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    env.read_env('.env.local')

    from tennisblock.settings.testing import *

else:
    env.read_env('.env.local')
    from tennisblock.settings.dev import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

