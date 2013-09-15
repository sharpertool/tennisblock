#!/usr/bin/env python

from Team import *

class Match(object):
    
    def __init__(self,t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def Diff(self):
        c1 = self.t1.Combined()
        c2 = self.t2.Combined()
        return abs(c1-c2)
        
    def Display(self):
        self.t1.Display()
        print "Versus"
        self.t2.Display()
        print "Diff: %4.2f\n" % self.Diff()

    def __repr__(self):
        return "%4.2f" % self.Diff()
        
