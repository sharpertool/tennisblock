
import glob
import os
import sys
import environ

env=environ.Env()

print("Loaded local_config from {}".format(__file__))
# Do an import * on the module version you would like to use

envfiles=glob.glob('.env') + glob.glob('*.env')
for envfile in envfiles:
    print("Reading environment from {}".format(envfile))
    env.read_env(envfile)

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    os.environ['USE_LESS'] = False
    os.environ['DEBUG'] = False
    from tennisblock.settings.testing import *

else:
    from tennisblock.settings.dev import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'tennisblock_flake'
    }
}

