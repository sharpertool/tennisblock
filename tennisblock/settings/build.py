from unipath import Path
print ("Running Build Settings.")

from .base import *

# These values are for the build process.
STATIC_SOURCE = PACKAGE_ROOT.child('static')
BUILD_JSBASEPATH = STATIC_SOURCE.child('js')

SECRET_KEY = 'reeG2vog5Ut5gaIc7Wed3ib5iSk4Yok'

