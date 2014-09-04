
print("Running staging settings.")

from .base import *

# Must define this key on the remote server
# Define in a local_settings.py file.
SECRET_KEY = ''

try:
    from local_settings import *
except ImportError:
    pass

