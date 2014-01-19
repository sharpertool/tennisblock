print ("Running Development Settings.")

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROD = False

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tennisblock_prod_mirror',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'tennisblock',
        'PASSWORD': 'P5HJTdHt5dR2t9Q2',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

SECRET_KEY = 'reeG2vog5Ut5gaIc7Wed3ib5iSk4Yok'


# Set this for development, but clear for PROD
BLOCK_NOTIFY_RECIPIENTS = ['ed@tennisblock.com','viquee@me.com']

try:
    from local_settings import *
except ImportError:
    print("No local settings file imported")

