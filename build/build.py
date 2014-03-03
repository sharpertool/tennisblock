#!/usr/bin/env python

import argparse
import os
from os.path import exists, join, dirname
import re
import sys
import subprocess
sys.path.append(join(dirname(__file__),'..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock.settings.build")
from django.conf import settings

from SharperTool.buildtools import ClosureCompiler,LessCompiler,CSSMinifier
from build_specifications import BuildSpec

def main():


    parser = argparse.ArgumentParser()

    parser.add_argument('--pretty',
                        action="store_true",
                        help="Enable pretty printing of the output.")

    parser.add_argument('--advanced',
                        action="store_true",
                        help="Enable advanced compilation.")

    parser.add_argument('--vmap',
                        help="Enable the Variable Map output file to the specified file.")

    args = parser.parse_args()

    print("Static Source Directory:" + settings.STATIC_SOURCE)

    spec = BuildSpec(settings.STATIC_SOURCE)
    build_spec = spec.getSpec()

    lessc = LessCompiler()
    minifier = CSSMinifier()

    for f,data in build_spec.iteritems():

        lessroot = join(settings.STATIC_SOURCE,'less')

        for spec in data.get('less',[]):
            lessc.compile(spec.get('src'),dest=spec.get('dest',None),paths=[lessroot])


        for spec in data.get('cssmin'):
            cssfiles = spec.get('src',[])
            dest = spec.get('dest')
            minifier.minify(cssfiles,dest)


if __name__ == '__main__':
    main()
