#!/usr/bin/env python
import os
import sys
import re

if __name__ == "__main__":

    setting = 'dev'
    m = re.match('setting:(\w+)',sys.argv[1])
    if m:
        setting = m.group(1)
        del sys.argv[1]
        print sys.argv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock.settings.%s" % setting)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
