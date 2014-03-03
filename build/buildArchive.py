#!/usr/bin/env python

import argparse
import os
import zipfile
import re

from directory_specifications import directory_specifications

from path import path

from build.utils import BuildUtil

def main():

    mypath = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.dirname(os.path.abspath(mypath)) # Climb to parent dir

    parser = argparse.ArgumentParser()

    parser.add_argument('--gz',
                        required=True,
                        help='Specify output gz file.')

    parser.add_argument('--dev',
                        action='store_true',
                        help='Set to perform a development build, including all source.')

    parser.add_argument('--rootdir',
                        default=rootdir,
                        help="Specify the root of the project directory.")

    args = parser.parse_args()

    if args.dev:
        build='dev'
    else:
        build='prod'

    spec = directory_specifications.get(build,{})

    z = BuildUtil()
    z.zipAll(args.rootdir,args.gz,spec)



if __name__ == '__main__':
    main()
