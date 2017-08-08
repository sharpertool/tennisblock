import environ
import os
import sys
from os.path import join, normpath

print("Loaded local_config from %s." % __file__)

env = environ.Env()

print("Argv length:{} Contents:{}".format(len(sys.argv), ",".join(sys.argv)))
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    print("Running test mode..")
    from tennisblock.settings.test import *
else:
    if env.bool('DJANGO_DOCKER', False):
        env.read_env('.env.local.docker')
    else:
        env.read_env('.env.local')

    from tennisblock.settings.dev import *

ALLOWED_HOSTS += [
    'tennis.local'
]
