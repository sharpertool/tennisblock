#!/usr/bin/env python

from Player import *
import random
import MySQLdb
from MySQLdb import *

def _printpair(m,f):
    print "%s %s (%3.1f/%3.1f) and %s %s (%3.1f/%3.1f) = %3.1f" % (m.first,m.last,m.ntrp,m.untrp,f.first,f.last,f.ntrp,f.untrp,m.untrp+f.untrp)

class TeamGen:
    
    def __init__(self,courts,nSeqs,men,women):
        self.courts = courts
        self.nSequences = nSeqs
        self.men = men
        self.women = women
        self.h2h = {}
        self.diffMax = 0.1
        self.MaxBadDiff = 1.0
        self.iterLimit = 10000
        self.Pairs = {}
        self.Opposites = {}
        self.Sequences = []
        
    def Restart(self):
        self.Pairs = {}
        self.Opposites = {}
        self.h2h = {}

    def GenerateSetSequences(self):
        n = self.courts * 2
        retries = 0
        self.Restart()
        self.diffMax = 0.1
        self.Sequences = []
        self.AcceptOneBadMatch  = False
        
        while (len(self.Sequences) < self.nSequences):
            goodMatch = False
            
            self.ClearCheckStats()
            while (goodMatch == False and self.diffMax <= 1.0):
                iterations = 0
                #numpy.random.seed()
                while (goodMatch == False and iterations < self.iterLimit):
                    pairIterations = 1
                    
                    #numpy.random.shuffle(ms)
                    self.chkOpposites = 0
                    self.chkPairs = 0
                    while True:
                        ms = self.GetSequence(self.men)
                        while self.CheckHead2Head(ms):
                            ms = self.GetSequence(self.men)
                            #numpy.random.shuffle(ms)
                    
                        fs = self.GetSequence(self.women)
                        #numpy.random.shuffle(fs)
                        while self.CheckHead2Head(fs):
                            fs = self.GetSequence(self.women)
                            #numpy.random.shuffle(fs)
                            
                        if not self.CheckPairsAndOpposites(ms,fs):
                            break
                            

                        pairIterations = pairIterations + 1
                        if pairIterations % 10000 == 0:
                            print "Tried %d Randomizations. Pairs:%d Opposites:%s" % (pairIterations,self.chkPairs,self.chkOpposites)
                            self.chkOpposites = 0
                            self.chkPairs = 0
                            
                    # At this point, we at least have a good group.                                
                    iterations = iterations + 1
                    if iterations % 1000 == 0:
                        print "Tried %d Iterations." % iterations
                    goodMatch = self.Check(ms,fs)
                
                if goodMatch == False:
                    self.diffMax = self.diffMax + 0.1
                    print "DiffMax Increased to %5.3f" % self.diffMax
            
            
            if goodMatch == True:
                seq = {'men':ms,'women':fs, 'diffMax':self.diffMax}
                self.Sequences.append(seq)
                self.UpdateSeqData(seq)
                dMax,dAvg, DiffList = self.DiffStats(seq)
                diffs = ",".join(["%5.3f" % x for x in DiffList])
                print "Found a sequence with Max:%3.3f Avg:%5.3f List:%s" % (dMax,dAvg,diffs)
            else:
                self.PrintCheckStats()
                random.shuffle(self.Sequences)
                s = self.Sequences.pop()
                dMax,dAvg, DiffList = self.DiffStats(s)
                diffs = ",".join(["%5.3f" % x for x in DiffList])
                print "Deleted a sequence with Max:%3.3f Avg:%5.3f List:%s" % (dMax,dAvg,diffs)
                
                retries = retries + 1
                self.Restart()
                for s in self.Sequences:
                    self.UpdateSeqData(s)
        
                self.diffMax = 0.1

            if retries == 20:
                return self.Sequences
            elif retries > 10:
                if len(self.Sequences) == (self.courts -1):
                    self.MaxBadDiff = self.MaxBadDiff + 0.1
                    self.AcceptOneBadMatch = True
                    print "Accepting a worse Max Diff of %5.3f" % self.MaxBadDiff
                else:
                    self.AcceptOneBadMatch = False
            elif retries > 5:
                if len(self.Sequences) == (self.courts -1):
                    self.AcceptOneBadMatch = True
                    print "Accepting a Max Diff of %5.3f" % self.MaxBadDiff
                else:
                    self.AcceptOneBadMatch = False
                
            print "Currently have %d sequences. Retries = %d" % (len(self.Sequences),retries)
        
        
        return self.Sequences
    
    def GetSequence(self,sin):
        x = range(0,len(sin))
        sout = []
        while x:
            i = random.randrange(0,len(x))
            r = x.pop(i)
            sout.append(sin[r])
        
        return sout
        
    
    def PrintCheckStats(self):
        print "Failed Stats:Pairs:%d Repeats:%d Matchup:%d" % (self.chkPairs,self.chkH2H,self.chkMatchups)

    def UpdateSeqData(self,seq):
        ms = seq['men']
        fs = seq['women']
        self.AddPairs(ms,fs)
        self.UpdateHead2Head(ms,fs)
    
    def AddPairs(self,ms,fs):
        for x in range(0,len(ms),2):
            m1 = ms[x]
            f1 = fs[x]
            m2 = ms[x+1]
            f2 = fs[x+1]
            
            self.Pairs[self.MakeKey(m1,f1)] = 1
            self.Pairs[self.MakeKey(m2,f2)] = 1
            self.Opposites[self.MakeKey(m1,f2)] = 1
            self.Opposites[self.MakeKey(m2,f1)] = 1
            
    def ClearCheckStats(self):
        self.chkPairs = 0
        self.chkH2H  = 0
        self.chkMatchups = 0
        
    def Check(self,ms,fs):
        if self.CheckPairsAndOpposites(ms,fs):
            self.chkPairs = self.chkPairs + 1
            return False
        
        if self.CheckHead2Head(ms):
            self.chkH2H = self.chkH2H + 1
            return False
        
        if self.CheckHead2Head(fs):
            self.chkH2H = self.chkH2H + 1
            return False
        
        if not self.CheckMatchup(ms,fs):
            self.chkMatchups = self.chkMatchups + 1
            return False
        
        return True
    
    def DiffStats(self,seq):
        ms = seq['men']
        fs = seq['women']
        diffMax = 0
        diffAvg = 0
        diffCnt = 0
        diffs = []

        for x in range(0,len(ms),2):
            m1 = ms[x]
            f1 = fs[x]
            m2 = ms[x+1]
            f2 = fs[x+1]
           
            t1 = m1.untrp + f1.untrp
            t2 = m2.untrp + f2.untrp
            
            diff = abs(t1-t2)
            diffCnt = diffCnt + 1
            diffAvg = diffAvg + diff
            if diff > diffMax:
                diffMax = diff
            diffs.append(diff)
                
        diffAvg = diffAvg/diffCnt
        diffs.sort()
        return diffMax,diffAvg,diffs
        

    def CheckMatchup(self,ms,fs): 
        n = self.courts * 2
        ok = False
        diffMax = 0
        diffAvg = 0
        diffCnt = 0
        
        badMatchups = 0
        
        for x in range(0,len(ms),2):
            m1 = ms[x]
            f1 = fs[x]
            m2 = ms[x+1]
            f2 = fs[x+1]
           
            t1 = m1.untrp + f1.untrp
            t2 = m2.untrp + f2.untrp
            
            diff = abs(t1-t2)
            diffCnt = diffCnt + 1
            diffAvg = diffAvg + diff
            if (diff > diffMax):
                diffMax = diff
                
            if diff > self.diffMax:
                if self.AcceptOneBadMatch:
                    # How bad..?
                    if badMatchups > 0:
                        print "Too many bad matchups."
                        return False
                        
                    if diff > self.MaxBadDiff:
                        print "Diff %5.3f too great." % diff
                        return False
                    
                    badMatchups = 1
                else:
                    return False
                
        diffAvg = diffAvg/diffCnt
        return True
        
    def CheckPairsAndOpposites(self,ms,fs):
        for x in range(0,len(ms),2):
            m1 = ms[x]
            f1 = fs[x]
            m2 = ms[x+1]
            f2 = fs[x+1]

            ''' Did they already play together? '''
            if self.Pairs.has_key(self.MakeKey(m1,f1)):
                self.chkPairs = self.chkPairs + 1
                return True
            if self.Pairs.has_key(self.MakeKey(m2,f2)):
                self.chkPairs = self.chkPairs + 1
                return True
            
            ''' Have they already played opposite each other? '''
            if self.Opposites.has_key(self.MakeKey(m1,f2)):
                self.chkOpposites = self.chkOpposites + 1
                return True
            if self.Opposites.has_key(self.MakeKey(m2,f1)):
                self.chkOpposites = self.chkOpposites + 1
                return True
            
        return False
    
    def CheckHead2Head(self,xs):
        for x in range(0,len(xs),2):
            x1 = xs[x]
            x2 = xs[x+1]
            
            k = self.MakeSortedKey(x1,x2)
            if self.h2h.has_key(k):
                return True
            
        return False
    
    def UpdateHead2Head(self,ms,fs):
        for x in range(0,len(ms),2):
            m1 = ms[x]
            f1 = fs[x]
            m2 = ms[x+1]
            f2 = fs[x+1]
            
            k = self.MakeSortedKey(m1,m2)
            self.h2h[k] = 1
            
            k = self.MakeSortedKey(f1,f2)
            self.h2h[k] = 1
    
    def MakeKey(self,a,b):
        #return a.pid * 1000 + b.pid
        #return "%03d:%03d" % (a.pid,b.pid)
        return "%s %s:%s %s" % (a.first,a.last,b.first,b.last)
        
    def MakeSortedKey(self,a,b):
        if a.pid < b.pid:
            return self.MakeKey(a,b)
        else:
            return self.MakeKey(b,a)
    
    def _printpair(self,m,f):
        print "%s %s (%3.1f/%3.1f) and %s %s (%3.1f/%3.1f) = %3.1f" % (m.first,m.last,m.ntrp,m.untrp,f.first,f.last,f.ntrp,f.untrp,m.untrp+f.untrp)

    def DisplaySequence(self,seq):
        set = 1
        for s in seq:
            print "Set %d" % set
            ms = s['men']
            fs = s['women']
            for x in range(0,len(ms),2):
                m1 = ms[x]
                f1 = fs[x]
                m2 = ms[x+1]
                f2 = fs[x+1]
                   
                self._printpair(m1,f1)
                print "Versus"
                self._printpair(m2,f2)
                print "Diff: %4.2f\n" % abs((m1.untrp+f1.untrp)-(f2.untrp+m2.untrp))
                
            set = set + 1
            
    def InsertRecords(self,conn,matchID,seq):
        '''
        '''
        
        curs = conn.cursor()
        
        set = 1
        for s in seq:
            print "Set %d" % set
            m = s['men']
            f = s['women']
            court = 1
            for x in range(0,len(m),2):
                m1 = m[x]
                f1 = f[x]
                m2 = m[x+1]
                f2 = f[x+1]
                
                _printpair(m1,f1)
                print "Versus"
                _printpair(m2,f2)
                print "Diff: %4.2f\n" % abs((m1.untrp+f1.untrp)-(f2.untrp+m2.untrp))
                
                positions = {
                    'tapa'  : m1.pid,
                    'tapb'  : f1.pid,
                    'tbpa'  : m2.pid,
                    'tbpb'  : f2.pid
                    }
                
                for position in positions.keys():
                    pid = positions[position]
                    sql = ("""
    insert into slots
        (matchid, setnum, court,pid,position,combokey)
    values (
        %d,
        %d,
        %d,
        %d,
        "%s",
        ""
    )
            """ % (matchID,set,court,pid,position))
                    
                    curs.execute(sql)
                court = court + 1
                
            set = set + 1
            
        conn.commit()
        
                
                