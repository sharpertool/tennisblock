import environ

print("Running Development Settings.")

env = environ.Env()

env("RAVEN_CONFIG", default='https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@sentry.io/29740')

from .common import *

DEBUG = True

ENABLE_DEBUG_TOOLBAR = DEBUG and env.str('ENABLE_DEBUG_TOOLBAR', default=False)

if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE += [
        'djdev_panel.middleware.DebugMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
        'django_nose',
    ]

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar', ]

STATICFILES_DIRS += [DJANGO_ROOT('static'),]


DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


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