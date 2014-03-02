
import os
from os.path import *
import zipfile
from path import path
import re

class BuildUtil(object):

    def __init__(self):
        self._globalcomp = []
        self._globalPats = []

    def setGlobalIgnore(self,ignorePats):
        """
        Compile the given global ignores into a series of patterns.
        """
        self._globalPats = ignorePats
        for pat in ignorePats:
            self._globalcomp.append(re.compile(pat))

    def testGlobalIgnore(self,file):
        """
        Test a file against the global ignore, return
        True to ignore, False to pass
        """
        for pat in self._globalcomp:
            if pat.match(file):
                return True

        return False

    def zipPath(self,zip,path,spec):
        """
        Zip files defined by the given spec.
        """
        ignorePatterns = []

        ignore = spec.get('ignore',None)
        if ignore:
            if type(ignore) is list:
                for i in ignore:
                    ignorePatterns.append(re.compile(i))
            else:
                ignorePatterns.append(re.compile(ignore))

        isIgnored = lambda f:any([pat.match(f) for pat in ignorePatterns])

        filepattern = spec.get('files','*')
        recursive   = spec.get('recursive',True)

        """ Do not apply global ignore to files specified by name """
        if type(filepattern) is list:
            for filename in filepattern:
                fullpath = os.path.join(path,filename)
                if os.path.exists(fullpath):
                    zip.write(fullpath)
        else:
            """ A pattern spec """
            if recursive:
                files = path.walk(filepattern)
            else:
                files = path.files(filepattern)

            for file in files:
                if not self.testGlobalIgnore(file) and not isIgnored(file):
                    zip.write(file)




    def zipAll(self, root, filename,spec,**kwargs):
        """
        Process the directory specification.

        The spec format is as follows:

         spec = {
            '<version>' : {
                'dirs' : {
                    # List of directory names
                    <dirname> : {
                        'files' : '*' # take all files from this dir
                        or
                        'files' : [ filename, filename,...,filename]
                        # If not specified, files defaults to all, recursive

                        'ignore' : '.*/eeweb/.*'
                        or
                        'ignore' : [ pattern1, pattern2, ... , patternN]
                    },
                'globalignore': [ ignorepat1, ignorepat2,...,ignorepatN]
                }
            }
        }

        """

        os.chdir(root)

        globalIgnores = spec.get('globalignore',[])
        self.setGlobalIgnore(globalIgnores)

        zip = zipfile.ZipFile(filename, 'w')

        for dir,dirspec in spec['dirs'].iteritems():
            p = path(os.path.join(dir))

            self.zipPath(zip,p,dirspec)

        for file in spec['files']:
            zip.write(file)

        zip.close()

