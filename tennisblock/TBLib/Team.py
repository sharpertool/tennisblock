#!/usr/bin/env python

class Team(object):
    
    def __init__(self,m,f):
        self.m = m
        self.f = f
        
    def Combined(self):
        return self.m.microntrp+self.f.microntrp
        
    def Display(self):
        m = self.m
        f = self.f
        print "%s %s (%3.1f/%3.1f) and %s %s (%3.1f/%3.1f) = %3.1f" % (m.first,m.last,m.ntrp,m.microntrp,f.first,f.last,f.ntrp,f.microntrp,m.microntrp+f.microntrp)

    def __repr__(self):
        return str(self.m) + ":" + str(self.f)
        
