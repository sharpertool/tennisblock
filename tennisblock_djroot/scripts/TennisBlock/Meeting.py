#!/usr/bin/env python

from MeetingStats import *

class Meeting(object):
    def __init__(self,nCourts,nSets,men,women):
        self.nCourts = nCourts
        self.nSets = nSets
        self.men = men
        self.women = women
        self.sets = []
        
        self.ms = MeetingStats(nCourts,nSets,men,women)
        
    def Restart(self):
        self.ms.Restart()
        self.sets = []
        
    def AddSet(self,set):
        self.sets.append(set)
        self.ms.AddSet(set)
        
    def Display(self):
        for set in self.ms.GetSets():
            setnum = 1
            print "Set %d" % setnum
            setnum = setnum + 1
            set.Display()
            
    def SetCount(self):
        return len(self.sets)
        
    def Check(self,set,diffMax):
        return self.ms.Check(set,diffMax)
        
    def GetNewSet(self,diffMax):
        self.ms.setCurrSetCount(len(self.sets))
        return self.ms.GetNewSet(diffMax)
 
    def PrintCheckStats(self):
        self.ms.PrintCheckStats()

    def DiffHistoryMin(self):
        return self.ms.DiffHistoryMin()

