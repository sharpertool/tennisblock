
print ("Running Production Settings.")

from .base import *

PROD = True

# This should be somewhere else...
STATIC_ROOT = PROJECT_ROOT.child('collectedstatic')

# Must define this key on the remote server
# Define in a local_settings.py file.
SECRET_KEY = ''

try:
    from local_settings import *
except ImportError:
    pass

