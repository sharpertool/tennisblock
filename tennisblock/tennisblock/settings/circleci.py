print("Circle CI Testing Settings")
import environ
import os
from os.path import exists, join

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 4
print(f"RootDir: {ROOT_DIR}")

# Allow testing to override a lot of variables at once.
envfile='.env.circleci'
if os.path.exists(envfile):
    print(f"Reading environment from {envfile}")
    env.read_env(envfile)

DEBUG = env.bool("DJANGO_DEBUG", default=False)

HOME_DIR = '/home/circleci/build'
if not exists(HOME_DIR):
    root = environ.Path(__file__) - 4
    HOME_DIR = root()

from .common import *

STATIC_ROOT = join(HOME_DIR, "collectedstatic")
MEDIA_ROOT = join(HOME_DIR, 'media')

STATICFILES_DIRS = [
    PROJECT_DIR('static')
]

POSTGRES_HOST = env('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = env('POSTGRES_PORT', default='5432')
POSTGRES_USER = env('POSTGRES_USER', default='circleci')
POSTGRES_DB = env('POSTGRES_DB', default='gardenbuzz')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default='testing-password')
DATABASES = {
    'default': env.db("DATABASE_URL",
                      default=f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'),
}

INSTALLED_APPS += (
    'coverage',
    'django_nose',
)

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

TEST_RUNNER = env('TEST_RUNNER', default='django_nose.NoseTestSuiteRunner')

NOSE_ARGS = [
    '--verbosity=2',
]

if env("NOSE_OUTPUT_FILE", default=False):
    NOSE_ARGS += [
        '--with-xunit',
        '--xunit-file={}'.format(env("NOSE_OUTPUT_FILE"))
    ]
