
import os
from os.path import join,exists,relpath,dirname,splitext,basename
import re
import platform
import subprocess
import tempfile
from cssmin import cssmin

def quote(f):
    return re.sub(' ','\\ ',f)

def dblquote(s):
    """ Wrap the string in quotes. """

    return '"%s"' % s


class BuildTool(object):



    def __init__(self):
        """
        Define the basic needs for the tool
        """

        self.tmpDir = '/tmp'
        self.tmpCss = 'build_min.css'


class CommandRunner(object):

    def __init__(self):
        self._sts = 0
        self._results = ""

    def joinfiles(self,files,out):
        """
        Join a list of files into a single file using 'cat'
        """

        if exists(out):
            os.unlink(out)

        FPO = open(out,'w')

        for file in files:
            if not exists(file):
                print("File {0} missing.".format(file))
                continue

            with open(file) as fp:
                FPO.write(fp.read())

    def minify(self,src,out):
        """
        Minify the given files.
        If the files are an array, then join them first, to avoid
        issues with the command shell length
        """
        tmpfile = "/tmp/_join_all_files.tmp"

        if isinstance(src,list):
            self.joinfiles(src,tmpfile)
            src = tmpfile

    def cmdPipe(self,cmd,display=False,stderr=False,**kwargs):
        """
        Run the given command in a pipe.
        Optionally print the results.

        Yes, there are multiple ways to run remote commands..

        """

        tmpfile = "/tmp/cmdPipe.err"
        if display:
            print(cmd)

        with open(tmpfile,'w') as errfile:

            if stderr:
                p = subprocess.Popen(cmd, shell=True,
                                     executable='/bin/bash',
                                     stdout=subprocess.PIPE,
                                     stderr=errfile)
                self._results = p.communicate()[0]
            else:
                p = subprocess.Popen(cmd, shell=True,
                                     executable='/bin/bash',
                                     stdout=subprocess.PIPE,
                                     stderr=errfile)

        self._sts = p.wait()
        self._results = p.communicate()[0]
        with open(tmpfile) as fp:
            self._err = fp.read()

        if self._sts:
            print("Error:{0}".format(self._err))
        if display:
            print(self._results)

        return self._results


    def call(self,proggy,args):
        """
        Prepend the EEWeb.scriptroot variable, then call the python script
        with the given arguments.
        """

        allargs = [proggy]
        allargs.extend(args)
        print("Calling " + proggy + " " + " ".join(args))
        self._sts = subprocess.call(allargs)
        if self._sts != 0:
            raise Exception("Error calling:\n\t%s" % " ".join(allargs))

    def checkPath(self,files,file,basePaths):

        cwd = os.getcwd()

        foundFile = True
        for basePath in basePaths:
            fullpath = os.path.relpath(os.path.join(basePath,file),cwd)
            if os.path.exists(fullpath):
                files.append(fullpath)
                foundFile = True
                break

        if not foundFile:
            print("File not found:%s" % file)

        return files

    def check_output(self,proggy,args):
        """
        I copied this out of the EEWeb package to eliminate that dependancy..
        """

        allargs = [dblquote(proggy)]
        allargs.extend(args)

        print("Running %s" % proggy)
        fullCmd = " ".join(allargs)
        print("Args: %s" % fullCmd)
        print("Command length:%s" % len(fullCmd))
        try:
            os.system(fullCmd)
            self._results = ""
            return self._results
        except Exception as e:
            raise Exception("Error (%s) calling:\n\t%s" % (e," ".join(allargs)))

    @property
    def status(self):
        return self._sts

    @property
    def results(self):
        return self._results

class ClosureCompiler(CommandRunner):

    def __init__(self):
        super(ClosureCompiler,self).__init__()
        self.cssmin = 'cssmin'
        self.java = self.findjava()
        self.closureJar = self.findclosurejar()

    def findjava(self):
        """
        Search a few known places for java..
        """

        if platform.system() == 'Windows':
            javabin = 'java.exe'
            pathsplit = ';'
        else:
            javabin = 'java'
            pathsplit = ':'

        checkpaths = os.getenv('PATH').split(pathsplit)

        checkpaths.extend([
            os.getenv('JAVA_HOME',''),
            os.path.join(os.getenv('JAVA_HOME',''),'bin'),
            ])

        for path in checkpaths:
            #print("Raw Path:%s" % path)
            java = os.path.join(path,javabin)
            #print("Checking:%s" % java)
            if os.path.exists(java):
                print("Using java from %s" % java)
                return java

        raise Exception("Unable to locate a valid java executable. Searched the following paths:%s" % ("\n\t".join(checkpaths)))

    def findclosurejar(self):
        """
        Use default args to find the closure jar
        """

        mypath = os.path.realpath(os.path.dirname(__file__))
        jarPath = os.path.relpath(os.path.join(mypath,'../jars','compiler.jar'))

        if os.path.exists(jarPath):
            return jarPath

        raise Exception("Could not find the default closure compiler jar file.")


    def closure_compile(self,jsFiles, outputFile,**kwargs):
        """
        Perform the compile step, using the passed in arguments
        """

        if len(jsFiles) == 0:
            raise Exception("No javascript files to compile")

        if os.path.exists(outputFile):
            print("Removed existing output file %s." % outputFile)
            os.unlink(outputFile)

        opts = ['-jar', quote(os.path.relpath(self.closureJar))]

        if kwargs.get('vmap',None):
            opts.extend(['--create_source_map', kwargs.get('vmap'), '--source_map_format=V3'])

        if kwargs.get('adv',False):
            opts.extend(['--compilation_level', 'ADVANCED_OPTIMIZATIONS'])
        else:
            opts.extend(['--compilation_level', 'SIMPLE_OPTIMIZATIONS'])

        if kwargs.get('pretty',False):
            opts.extend(['--formatting', 'PRETTY_PRINT',
                         '--formatting', 'PRINT_INPUT_DELIMITER'])

        tmpfile = '/tmp/closure_compiler_jsinput_tmp.js'
        self.joinfiles(jsFiles,tmpfile)

        jsOpts = []
        jsOpts.append('--js')
        jsOpts.append(tmpfile)

        opts.extend(jsOpts)

        opts.append('--js_output_file')
        opts.append(quote(outputFile))

        results = self.check_output(self.java,opts)
        print results

        os.unlink(tmpfile)

        if not os.path.exists(quote(outputFile)):
            print("Output file (%s) was not generated properly" % outputFile)


    def parsemxClient(self,basepath,mxClientFile):
        """
        Get a list of files that the mxClient.js top level file imports so I can pass
        them all to the closure compiler. Closure requires a list of files one at a time.

        """

        cwd = os.getcwd()
        mxClient = []
        files = []

        if os.path.exists(mxClientFile):
            fp = open(mxClientFile,'r')
        elif os.path.exists(os.path.join(basepath,mxClientFile)):
            fp = open(os.path.join(basepath,mxClientFile),'r')

        bEndOfHeader = False
        for line in fp:
            m = re.search('^mxClient\.include\(mxClient.basePath\+\'\/(.*)\'\);',line)
            if m:
                bEndOfHeader = True
                file = m.group(1)
                fullpath = os.path.join(basepath,file)
                if os.path.exists(fullpath):
                    rp = os.path.relpath(fullpath,cwd)
                    files.append(rp)
                else:
                    print("File not found:%s" % fullpath)
            else:
                if not bEndOfHeader:
                    mxClient.append(line)

        fp.close()

        # Save to mxClient_header.js file
        hdrFile = os.path.join(os.path.dirname(mxClientFile),'mxClient_header.js')
        fp = open(hdrFile,'w')
        for line in mxClient:
            fp.write(line)
        fp.close()


        files.insert(0,hdrFile)
        return files

    def parseClientFile(self,basepath,ClientFile):
        """
        Get a list of files that the dkClient.js top level file imports so I can pass
        them all to the closure compiler. Closure requires a list of files one at a time.

        """

        cwd = os.getcwd()
        files = []

        if os.path.exists(ClientFile):
            fp = open(ClientFile,'r')
        elif os.path.exists(os.path.join(basepath,ClientFile)):
            fp = open(os.path.join(basepath,ClientFile),'r')

        bEndOfHeader = False
        for line in fp:
            m = re.search('"(.*)"',line)
            if m:
                file = m.group(1)
                if file == "/js/":
                    continue

                fullpath = os.path.join(basepath,file)
                if os.path.exists(fullpath):
                    rp = os.path.relpath(fullpath,cwd)
                    files.append(rp)
                else:
                    print("File not found:%s" % fullpath)

        fp.close()

        return files

class CSSMinifier(CommandRunner):

    def __init__(self):
        pass

    def minify(self,cssfiles,out):
        """
        Minify a list of css files into a single, minified file.
        """

        if isinstance(cssfiles,list):
            files = cssfiles
        else:
            files = [cssfiles]

        tmpfile = '/tmp/css_minifier.css'
        self.joinfiles(cssfiles,tmpfile)

        import cssmin
        output = cssmin.cssmin(open(tmpfile).read())
        with open(out,'w') as fp:
            fp.write(output)


class LessCompiler(CommandRunner):
    """
        Compile and minify lesss files
    """

    def __init__(self):
        super(LessCompiler, self).__init__()

        self.node =  '/usr/local/bin/node'
        self.lessc = '/usr/local/bin/lessc'

    def compile(self,src,dest=None,paths=[],**kwargs):
        """
        Compile the given source file
        """


        cwd = os.getcwd()

        relpaths = [relpath(p,cwd) for p in paths]

        lesspath = ":".join(relpaths)

        # Source file relative to our current working directory
        src_relative = join(relpath(dirname(src),cwd),basename(src))
        if dest:
            dest_relative = join(relpath(dirname(dest),cwd),basename(dest))
        else:
            file,ext = splitext(basename(src))
            dfile = file + '.css'
            dest_relative = join(relpath(dirname(src),cwd),dfile)

        print ("Building {0} from {1}".format(dest_relative,src_relative))

        if os.path.exists(dest_relative):
            os.unlink(dest_relative)
        opts = [self.node,self.lessc]

        if paths:
            opts.append('--include-path=%s' % lesspath)
        opts.append(src_relative)
        opts.append('>|')
        opts.append(dest_relative)

        self.cmdPipe(" ".join(opts),display=True)

        if not self.status == 0:
            print("Failed to build destination file!")
        else:
            print("Built %s" % os.path.relpath(dest_relative))


