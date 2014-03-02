#!/usr/bin/env python

import argparse
import os
from os.path import exists, join, dirname
import re
import sys
import subprocess
sys.path.append(join(dirname(__file__),'..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schematics.settings.build")
from django.conf import settings

from AspenLabs.buildtools import ClosureCompiler,LessCompiler,CSSMinifier
from build_specifications import BuildSpec

class ClientCompiler(ClosureCompiler):

    def __init__(self,spec):
        super(ClientCompiler,self).__init__()

        self.clientFile = spec.get('src')
        self.preFiles = spec.get('pre',[])
        self.postFiles = spec.get('post',[])
        self.destFile = spec.get('dest')
        self.basepath = spec.get('basepath','')

        self._parser = self.parseClientFile

    def mxcompile(self,**kwargs):
        """
        Set the parse function and call the compile.
        """
        self._parser = self.parsemxClient
        return self.compile(**kwargs)

    def compile(self,vmap=False,adv=False,pretty=False):
        """
        Assemble required files, and call the closure compiler.
        """

        jsFiles = []

        for f in self.preFiles:
            if exists(f):
                jsFiles.append(f)

        if exists(self.clientFile):
            files = self._parser(self.basepath,self.clientFile)
            jsFiles.extend(files)
        else:
            print("Specified client file (%s) was not found." % self.clientFile)

        for jsfile in self.postFiles:
            jsFiles.append(jsfile)

        if len(jsFiles) == 0:
            print("No javascript files were found to process.")
            print("The current directory is %s" % os.getcwd())
            print("The specified basepath is %s" % settings.BUILD_EEBASEPATH)
            print("Insure that the base path and the files in the import list combined will be valid.")
            sys.exit(2)

        self.closure_compile(jsFiles,self.destFile)


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

    spec = BuildSpec(settings.STATIC_SOURCE,settings.BUILD_MXROOT)
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

        """ Compile the client javascript files """
        spec = data.get('client')
        spec['basepath'] = settings.BUILD_EEBASEPATH
        clientComp = ClientCompiler(spec)
        clientComp.compile(vmap=args.vmap,adv=args.advanced,pretty=args.pretty)

        """ Compile the mxGraph javascript library """
        spec = data.get('mxgraph')
        if spec:
            spec['basepath'] = settings.BUILD_MXBASEPATH
            mxComp = ClientCompiler(spec)
            mxComp.mxcompile(vmap=args.vmap,adv=args.advanced,pretty=args.pretty)



if __name__ == '__main__':
    main()
