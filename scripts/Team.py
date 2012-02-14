#!/usr/bin/env python

from Player import *

class Team:
    
    def __init__(self,m,f):
        self.m = m
        self.f = f
        
    def Combined(self):
        return self.m.untrp+self.f.untrp        
        
    def Display(self):
        m = self.m
        f = self.f
        print "%s %s (%3.1f/%3.1f) and %s %s (%3.1f/%3.1f) = %3.1f" % (m.first,m.last,m.ntrp,m.untrp,f.first,f.last,f.ntrp,f.untrp,m.untrp+f.untrp)

    def __repr__(self):
        return str(self.m) + ":" + str(self.f)
        
