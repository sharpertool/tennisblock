import json
import argparse
import re
import glob
import fnmatch
import path
import os
from os.path import join,basename,dirname,relpath,abspath
from PIL import Image


from django.db import connection
from blockdb.models import *

import os
os.environ['PYTHONPATH'] = '../../gbrest'
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings'
import tennisblock_dj.settings

