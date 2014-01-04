
print("Running staging settings.")

from .base import *

try:
    from local_settings import *
except ImportError:
    print("No local settings file imported")

