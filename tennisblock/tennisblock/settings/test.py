
print ("Running Test Settings.")

from .base import *

DATABASES['default']['NAME'] = 'tennisblock_test'

try:
    from local_settings import *
except ImportError:
    pass

