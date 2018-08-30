
print ("Running Test Settings.")

from .common import *

DATABASES['default']['NAME'] = 'tennisblock_test'

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://d5b96362c1574d68bf050ecfd8d4a2f4:8024bcdfe7b143acab9be3ad4ba38118@app.getsentry.com/29740',
    }

