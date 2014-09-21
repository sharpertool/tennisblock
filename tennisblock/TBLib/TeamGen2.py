#!/usr/bin/env python

from .Meeting import Meeting

class TeamGen(object):

    def __init__(self,courts, num_seq, men, women):
        self.nCourts = courts
        self.meeting = Meeting(courts, num_seq, men,women)
        self.diffMax = 0.1
        self.MaxBadDiff = 1.0
        self.nSequences = num_seq
        self.iterLimit = 1000

    def generate_set_sequences(self,dups):
        self.meeting.Restart()
        diff_max = 0.1

        self.meeting.ms.setSeeGirlsOnce(dups)

        while self.meeting.SetCount() < self.nSequences:
            set = None

            while diff_max <= 2.8 and set is None:
                set = self.meeting.GetNewSet(diff_max)


                if set is None:
                    diff_max = self.meeting.DiffHistoryMin()
                    print "DiffMax Increased to %5.3f" % diff_max


            if set is None:
                self.meeting.PrintCheckStats()
                print "Failed to build the sequence."
                return None
            else:
                set.Display()
                d_max, d_avg, diff_list = set.DiffStats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                print "Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (self.diffMax, d_max, d_avg, diffs)
                self.meeting.AddSet(set)

        return self.meeting.sets

    def display_sequences(self,seq):
        for s in seq:
            s.Display()


    def show_all_diffs(self,seq):
        [s.showDiffs() for s in seq]


