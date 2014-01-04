
print ("Running Test Settings.")

from .base import *

try:
    from local_settings import *
except ImportError:
    print("No local settings file imported")

