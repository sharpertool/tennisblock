# -*- coding: utf-8 -*-

import environ
import os
from os.path import exists, join

env = environ.Env()

default_env = env.str('DEFAULT_ENV_FILE', default='.env')

def read_env(file=default_env):
    """ Search PYTHONPATH for given file and load first one found """
    print(f"reading from default file {file}")

    # Add the current directorory to the paths
    search_paths = [os.curdir] + env.str('PYTHONPATH', default='').split(':')

    # Search the python path for 1 or more envfiles, and load the first one
    l = lambda x: join(x, file)
    envfiles = [f for f in
                map(l, search_paths)
                if exists(f)]

    if envfiles:
        print(f"Found {len(envfiles)} file(s). Using {envfiles[0]}")
        file = envfiles[0]
        env.read_env(file, overwrite=True)
    else:
        print("Found no environment files!")

