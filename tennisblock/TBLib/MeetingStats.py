#!/usr/bin/env python

import sys
from Team import *
from Match import *
from Set import *
from Meeting import *

import random

def MakeKey(m,f):
    #return a.pid * 1000 + b.pid
    #return "%03d:%03d" % (a.pid,b.pid)
    return "%s %s:%s %s" % (m.first,m.last,f.first,f.last)

def MakeSortedKey(a,b):
    if a.pid < b.pid:
        return MakeKey(a,b)
    else:
        return MakeKey(b,a)

class MeetingStats(object):

    def __init__(self,nCourts,nSets,men,women):
        self.nCourts = nCourts
        self.nSets = nSets
        self.men = men
        self.women = women
        self.nCurrSetCount = 0

        self.maxIterations = 100

        self.seeGirlsOnlyOnce = False
        if self.nCourts == 3:
            self.seeGirlsOnlyOnce = False

        self.chkMatchups = 0
        self.chkH2H = 0
        self.chkPairs = 0

        self.Opponents = {}
        self.Partners = {}
        self.Opposites = {}
        self.Opposites2X = {}
        self.InvalidFemOpponents = {}
        self.InvalidFemPartners = {}

        self.specialCase = self.isSpecialCase()

        self.minDiffHistory = []


        # Need a reverse lookup table
        self.pbyname = {}
        for p in self.men+self.women:
            self.pbyname[p.Name()] = p

    def setSeeGirlsOnce(self,bTrue):
        if bTrue:
            print("Setting the see Girls seeting to True")
            self.maxIterations *= 10
        else:
            print("Setting the see Girls seeting to False")
        self.seeGirlsOnlyOnce = bTrue

    def setMaxIteration(self,n):

        self.maxIterations = n

    def setCurrSetCount(self,n):
        self.nCurrSetCount = n

    def Restart(self):
        """
        Clear all statistics and restart the checking
        """

        self.Partners = {}
        self.Opponents = {}
        self.Opposites = {}
        for p in self.men+self.women:
            self.Partners[p.Name()] = set()
            self.Opposites[p.Name()] = set()
            self.Opponents[p.Name()] = set()
            self.Opposites2X[p.Name()] = set()
        for p in self.men:
            self.InvalidFemOpponents[p.Name()] = set()

            self.InvalidFemPartners[p.Name()] = set()

        print "Restart Done"


    def isSpecialCase(self):
        """
        Grrr - this is special for Sheryl, who asks to play with Kirby!
        Hah!!! Mike isn't on our block, and neither is Sheryl/
        """
        return False
        for m in self.men:
            if m.Name() == 'Dickhead':
                for w in self.women:
                    if w.Name() == 'Vagina':
                        return True
        return False

    def DiffHistoryMin(self):
        return min(self.minDiffHistory)

    def AddSet(self,set):
        """
        Once we have a valid set, then add it to the list and update
        all of the variables we use to track the statisics for this run.

        """
        for match in set.matches:
            m1 = match.t1.m.Name()
            f1 = match.t1.f.Name()
            m2 = match.t2.m.Name()
            f2 = match.t2.f.Name()

            # Do both directions
            self.Opponents[m1].add(m2)
            self.Opponents[m2].add(m1)
            self.Opponents[f1].add(f2)
            self.Opponents[f2].add(f1)

            # Do partners m->f
            self.Partners[m1].add(f1)
            self.Partners[m2].add(f2)

            # Do opposites
            if f2 in self.Opposites[m1]:
                self.Opposites2X[m1].add(f2)
            else:
                self.Opposites[m1].add(f2)

            if f1 in self.Opposites[m2]:
                self.Opposites2X[m2].add(f1)
            else:
                self.Opposites[m2].add(f1)

        for m in self.men:
            mn = m.Name()
            if self.seeGirlsOnlyOnce:
                m_invalid = self.Partners[mn].union(self.Opposites[mn])
            else:
                m_invalid = self.Partners[mn].intersection(self.Opposites[mn])
                m_invalid = m_invalid.union(self.Opposites2X[mn])
            self.InvalidFemOpponents[mn] = m_invalid

            if self.seeGirlsOnlyOnce:
                p_invalid = self.Partners[mn].union(self.Opposites[mn])
            else:
                p_invalid = self.Partners[mn].union(self.Opposites2X[mn])
            self.InvalidFemPartners[mn] = p_invalid

        print "Added a set"

    def GetSets(self):
        return self.sets

    def ClearCheckStats(self):
        self.nFailuresByInvalidPartner = 0
        self.nFailuresByDiff  = 0
        self.minDiff = 10

    def PrintCheckStats(self):
        print "Failed Stats:Partner:%d Diff:%d Mindiff:%4.2f" \
            % (self.nFailuresByInvalidPartner,self.nFailuresByDiff,self.minDiff)

    def GetNewSet(self,diffMax):
        """
        This one needs to use the existing sets and list and pick a new randomization
        of the available sets.
        """

        """
        - Pick a guy
            - Pick an opponent from list of available opponents - men not played yet
            - Pick two women from list of available women (checking opposites, pairs)
        - From remaining guys, repeat the above.. and then for the last set
        """
        tries = 0
        maxTries = 1

        while tries < maxTries:
            print "Trying to build a set DiffMax:%5.3f Try # %d." % (diffMax,tries)
            s = self.BuildSet(diffMax)
            if s:
                return s

            tries = tries + 1

        return None

    def getTempList(self):

        t_men = [x.Name() for x in self.men]
        t_women = [x.Name() for x in self.women]
        return  t_men,t_women

    def initSet(self,t_men):
        """
        Build a new set with a list of men that are valid opponents of each other.

        Each time this function is called, a new random set of men should be chosen.
        The only history used is the history of men that have played against each other
        this night. The ValidOpponent function is used for this determination.
        """
        newSet = Set()
        s_men = set(t_men)

        for n in range(0,self.nCourts):
            m1 = random.choice(list(s_men))
            s_men.remove(m1)
            m2 = self.ValidOpponent(m1,s_men)
            s_men.remove(m2)
            m = Match(Team(self.pbyname[m1],None),Team(self.pbyname[m2],None))
            newSet.AddMatch(m)
        return newSet

    def BuildSet(self,diffMax):
        """
        First, build a set of matches with men only.
        Next, add in the women. The men are assigned
        randomly, so it should not matter what the women
        are assigned as later.. they will be assigned
        randomly to the men.
        """
        nTries = 0
        maxTries = self.maxIterations

        self.minDiffHistory = []

        self.setList = []

        while nTries < maxTries/10:
            t_men,t_women = self.getTempList()

            # Build sets of men first.
            # If there is an exception thrown, then just ignore
            # it and try again..
            while True:
                try:
                    newSet = self.initSet(t_men)
                    break
                except:
                    pass

            print "Assigned men. Try to assign women. Seqs:%d Try:%d Diff=%5.3f" % (self.nCurrSetCount,nTries,diffMax)
            self.ClearCheckStats()
            if self.AddWomen(newSet,t_women,diffMax,self.maxIterations):
                return newSet
            self.PrintCheckStats()
            self.minDiffHistory.append(self.minDiff)
            nTries = nTries + 1

        return None

    def AddWomen(self,aset,t_women,diffMax,maxTries):
        """
        Upon entry, aset will be a set that contains
        the male pairings, but with no women entered. The
        male pairings will have been done randomly, so
        they should be okay.
        """

        nTries = 0
        nContinue = True
        while nContinue and nTries < maxTries:
            s_women = set(t_women)
            random.seed()
            special_girl = None
            special_boy = None
            try:
                if self.specialCase and self.nCurrSetCount == 2:
                    # First set, make sure the special girl plays with
                    # the special boy
                    #special_girl = 'Sheryl Putnam'
                    #special_boy = 'Mike Kirby'
                    if special_girl in self.Partners[special_boy]:
                        special_girl = None
                        special_boy = None
                    else:
                        s_women.remove(special_girl)

                for m in aset.matches:
                    m.t1.f = None
                    m.t2.f = None

                    m1 = m.t1.m.Name()
                    m2 = m.t2.m.Name()
                    f1 = None
                    f2 = None

                    """
                    If this is the special case, then force them
                    together. This of course does not work if
                    they already played together!! I need to compensate
                    for that case.
                    """
                    if special_girl:
                        if m1 == special_boy:
                            f1 = special_girl
                            special_girl = None
                        elif m2 == special_boy:
                            f2 = special_girl
                            special_girl = None

                    if not f1:
                        f1 = self.ValidPartner(m1,m2,s_women,None)
                        s_women.remove(f1)
                    if not f2:
                        f2 = self.ValidPartner(m2,m1,s_women,f1)
                        s_women.remove(f2)
                    m.t1.f = self.pbyname[f1]
                    m.t2.f = self.pbyname[f2]

                currDiff = aset.Diff()
                if max(currDiff) <= diffMax:
                    return True
                self.minDiff = min(self.minDiff,max(currDiff))
                self.nFailuresByDiff = self.nFailuresByDiff + 1
                self.setList.append(aset.Clone())
            except:
                pass # Just do this for now.. we will restat anyway
                self.nFailuresByInvalidPartner = self.nFailuresByInvalidPartner + 1

            ## We have a bad one..
            nTries = nTries + 1

        # If we make it here.. we failed
        return False


    def ValidPartner(self,m1,m2,s_women,f1=None):
        """
        Pick a woman that is a valid partner for the two men specified in m1 and m2.

        The rule is -
        If a woman has played with AND against m2, she is not a valid opponent
        M2 will have seen her 3 times.
        Also if she has played against M2 2x already, she can't play against him again.

        f1 is set to the first female in the current group if this is the second call.
        """

        #m2_invalid = self.Partners[m2].intersection(self.Opposites[m2])
        #m2_invalid = m2_invalid.union(self.Opposites2X[m2])
        m2_invalid = self.InvalidFemOpponents[m2];

        #s_invalid = self.Partners[m1].union(self.Opposites2X[m1])
        m1_invalid = self.InvalidFemPartners[m1]
        s_invalid = m1_invalid.union(m2_invalid)

        if f1:
            s_invalid = s_invalid.union(self.Opponents[f1])

        tmp = s_women.difference(s_invalid)
        if len(tmp) == 0:
            raise Exception("No Valid Partner!")

        partner = random.choice(list(tmp))
        return partner

    def ValidOpponent(self,player,ssPlayers):
        """
        The difference line retrieves a list of same-sex players that have
        not been opponents to this player yet.

        Implements the rule that men only play against other men
        once, and women only play against other women once.

        """

        tmp = ssPlayers.difference(self.Opponents[player])
        if len(tmp) == 0:
            raise Exception("No Valid Opponent")

        opponent = random.choice(list(tmp))
        return opponent
