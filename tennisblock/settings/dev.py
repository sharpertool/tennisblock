print ("Running Development Settings.")

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROD = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tennisblock_prod_mirror',
        'USER': 'tennisblock',
        'PASSWORD': 'P5HJTdHt5dR2t9Q2',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = 'reeG2vog5Ut5gaIc7Wed3ib5iSk4Yok'

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@app.getsentry.com/29740',
}


# Set this for development, but clear for PROD
BLOCK_NOTIFY_RECIPIENTS = ['ed@tennisblock.com','viquee@me.com']

try:
    from local_settings import *
except ImportError:
    pass

