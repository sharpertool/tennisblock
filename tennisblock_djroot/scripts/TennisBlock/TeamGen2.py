#!/usr/bin/env python

from Meeting import *

class TeamGen(object):

    def __init__(self,courts,nSeqs,men,women):
        self.nCourts = courts
        self.meeting = Meeting(courts,nSeqs,men,women)
        self.diffMax = 0.1
        self.MaxBadDiff = 1.0
        self.nSequences = nSeqs
        self.iterLimit = 1000

    def GenerateSetSequences(self,dups):
        retries = 0
        self.meeting.Restart()
        diffMax = 0.1

        self.meeting.ms.setSeeGirlsOnce(dups)

        while (self.meeting.SetCount() < self.nSequences):
            set = None

            while diffMax <= 2.8 and set == None:
                set = self.meeting.GetNewSet(diffMax)


                if set == None:
                    diffMax = self.meeting.DiffHistoryMin()
                    #diffMax = diffMax + 0.1
                    print "DiffMax Increased to %5.3f" % diffMax


            if set == None:
                self.meeting.PrintCheckStats()
                print "Failed to build the sequence."
                return None
            else:
                set.Display()
                dMax,dAvg, DiffList = set.DiffStats()
                diffs = ",".join(["%5.3f" % x for x in DiffList])
                print "Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (self.diffMax,dMax,dAvg,diffs)
                self.meeting.AddSet(set)

        return self.meeting.sets

    def DisplaySequences(self,seq):
        for s in seq:
            s.Display()


    def showAllDiffs(self,seq):
        [s.showDiffs() for s in seq]


