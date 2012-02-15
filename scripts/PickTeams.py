#!/usr/bin/env python

import sys
#import getpass, imaplib
import os
import sys
#import email
import errno
import mimetypes
import re
import smtplib
from TeamGen2 import TeamGen

#os.environ['PYTHON_EGG_CACHE'] = "/tmp/tennis-eggs"

from Player import *
from optparse import OptionParser

from DBTeams import *

def PickTeams(fp,dbTeam,nCourts,nSequences,testing=False):

    men,women = dbTeam.getPlayers()

    tg = TeamGen(nCourts,nSequences,men,women)
    sequences = tg.GenerateSetSequences()

    if sequences == None or len(sequences) < nSequences:
        fp.write("Could not generate the required sequences.")

    else:
        # Put the worst sequences last.
        sequences.reverse()
        tg.DisplaySequences(sequences)
        tg.showAllDiffs(sequences)

        if not testing:
            dbTeam.InsertRecords(sequences)

    fp.write("Done")

def main():

    usage = "usage: %prog -n -m -s]"
    parser = OptionParser(usage)
    parser.add_option("-m", dest="matchid",
                      action="store",
                      type="int",
                      help="Matchid to schedule.")
    parser.add_option("-c", dest="courts",
                      action="store",
                      type="int",
                      default=4,
                      help="Number of courts.")
    parser.add_option("-s", dest="sequences",
                      action="store",
                      type="int",
                      default=3,
                      help="Number of sequences.")
    parser.add_option("-f",dest="outfile",
                       action="store",
                       type="string",
                       default="/tmp/schedule.log",
                       help="File to output debug data to")
    parser.add_option("-v",action="store_false",dest="verbose")
    parser.add_option("-t",action="store_true",dest="test")

    (options, args) = parser.parse_args()

    fp = sys.stdout

    try:
        if options.matchid:
            dbTeams = DBTeams(options.matchid)
        else:
            dbTeams = DBTeams()
    except:
        print("Could not open a DB Connection.")
        sys.exit(2)

    fp.write("Scheduling for Matchid:%s\n" % dbTeams.matchid)

    PickTeams(fp,
        dbTeams,
        options.courts,
        options.sequences,
        options.test)

    fp.close()

if __name__ == '__main__':
    main()
