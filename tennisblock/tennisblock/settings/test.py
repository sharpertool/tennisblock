
print ("Running Test Settings.")

from .base import *

try:
    from local_settings import *
except ImportError:
    pass

