
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

from optparse import OptionParser

from DBTeams import *

class TeamManager(object):

    def __init__(self,matchid = None):

        self.dbTeams = DBTeams()

    def pickTeams(self,date=None,**kwargs):

        isTesting = kwargs.get('test',True)
        noDupes = kwargs.get('nodupes',False)
        nCourts = kwargs.get('courts',3)
        nSequences = kwargs.get('sequences',3)

        men,women = self.dbTeams.getPlayers(date)

        if len(men) < nCourts*2 or len(women) < nCourts*2:
            errmsg = "Cannot pick teams, there are not enough men or women."
            errmsg += "Need %d of both. Have %d men and %d women." % (nCourts*2,len(men),len(women))
            return {"status" : {"error" : errmsg}}

        tg = TeamGen(nCourts,nSequences,men,women)
        sequences = tg.GenerateSetSequences(noDupes)

        if sequences == None or len(sequences) < nSequences:
            return {"status" : {"error" : "Could not generate the required sequences"}}

        else:
            # Put the worst sequences last.
            sequences.reverse()
            tg.DisplaySequences(sequences)
            tg.showAllDiffs(sequences)

            if not isTesting:
                self.dbTeams.InsertRecords(date,sequences)

            return sequences

    def queryMatch(self,date=None):

        matchdata = self.dbTeams.queryMatch(date)
        return matchdata

def main():

    # Do some testing
    pass

if __name__ == '__main__':
    main()
