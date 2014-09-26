from .MeetingStats import MeetingStats

class Meeting(object):
    def __init__(self, nCourts, nSets, men, women):
        self.nCourts = nCourts
        self.nSets = nSets
        self.men = men
        self.women = women
        self.sets = []
        
        self.ms = MeetingStats(nCourts, nSets, men, women)
        
    def Restart(self):
        self.ms.Restart()
        self.sets = []
        
    def AddSet(self,blockset):
        self.sets.append(blockset)
        self.ms.AddSet(blockset)
        
    def Display(self):
        for index, blockset in enumerate(self.ms.GetSets()):
            print "Set %d" % index+1
            blockset.Display()
            
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

