
print ("Running Test Settings.")

from .base import *

PROD = True

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tennisblock',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'tennisblock',
        'PASSWORD': 'P5HJTdHt5dR2t9Q2',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Must define this key on the remote server
# Define in a local_settings.py file.
SECRET_KEY = ''

try:
    from local_settings import *
except ImportError:
    pass

