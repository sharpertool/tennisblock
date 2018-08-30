
print ("Running Production Settings.")

from .common import *

ADMINS = (
    ('Ed Henderson', 'ed@tennisblock.com'),
)

DATABASES['default']['NAME'] = 'tennisblock'

# This should be somewhere else...
STATIC_ROOT = PROJECT_ROOT.child('collectedstatic')

# Must define this key on the remote server
# Define in a local_settings.py file.
SECRET_KEY = ''

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://bb218b1fa4274266aea0a33a4a10c0a5:9772e132d1904c99909fc13e2fc16da7@app.getsentry.com/24185',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'secure.emailsrvr.com'
EMAIL_PORT = 465

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'tennisblock_prod_flake'
    }
}

