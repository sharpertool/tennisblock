
import os
print ("Running Development Settings.")

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROD = False

INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE_CLASSES += \
    ("debug_toolbar.middleware.DebugToolbarMiddleward",)

