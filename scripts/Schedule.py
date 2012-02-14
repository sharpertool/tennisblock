#!/usr/bin/env python

import sys
import getpass, imaplib
import os
import sys
import email
import errno
import mimetypes
import re
import smtplib

os.environ['PYTHON_EGG_CACHE'] = "/tmp/tennis-eggs"

from optparse import OptionParser
import MySQLdb
from MySQLdb import *

def DBData(fp):
    conn = MySQLdb.connect(host='localhost', user='fntennis', passwd='k2baby')
    
    curs = conn.cursor()
    
    curs.execute('use friday_tennis')
    
    ret = curs.execute('select * from players')
    
    print "Number of rows %d<p>\n" % curs.rowcount
    
    colnames = [desc[0] for desc in curs.description]
    players = [dict(zip(colnames,row)) for row in curs.fetchall()]
    
    fp.write("pid,First,Last,Gender,NTRP,uNTRP,Cell,Home,E-mail\n")
    ret = curs.execute('select * from players')
    
    for player in players:
        pdata = [player[k] for k in ['PID','firstname','lastname','gender','NTRP','microNTRP','cell','home','email']]
        s = "%ld,%s,%s,%s,%f,%f,%s,%s,%s\n" % (pdata[0],pdata[1],pdata[2],pdata[3],pdata[4],pdata[5],pdata[6],pdata[7],pdata[8])
        fp.write(s)        
    
def main():
    
    usage = "usage: %prog --course <course> --labs LabNN[,LabNN] [--dir <labdir> --grades <grading excel file> -v]"
    parser = OptionParser(usage)
    parser.add_option("-m", dest="matchid",
                      action="store",
                      type="string",
                      help="Matchid to schedule.")
    parser.add_option("-f",dest="outfile",
                       action="store",
                       type="string",
                       default="/tmp/schedule.log",
                       help="File to output debug data to")
    parser.add_option("-v",action="store_false",dest="verbose")
    
    (options, args) = parser.parse_args()

    fp = open(options.outfile,"a")

    if options.matchid:
        fp.write("Scheduling for Matchid:%s\n" % options.matchid)

    DBData(fp)    
    
    fp.close()

if __name__ == '__main__':
    main()

