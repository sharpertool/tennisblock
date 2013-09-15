#!/usr/bin/env python

class Player:
    
    def __init__(self,pdata):
        
        self.pid = pdata['id']
        self.first = pdata['first']
        self.last  = pdata['last']
        self.gender = pdata['gender']
        self.ntrp = pdata['ntrp']
        self.untrp = pdata['microntrp']
        self.name = self.first + " " + self.last
        
    def Name(self):
        return self.name

    def __repr__(self):
        return "%s %4.2f (%4.2f)" % (self.name,self.ntrp,self.untrp)
        

