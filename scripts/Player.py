#!/usr/bin/env python

class Player:
    
    def __init__(self,pdata):
        
        self.pid = pdata['pid']
        self.first = pdata['firstname']
        self.last  = pdata['lastname']
        self.gender = pdata['gender']
        self.ntrp = pdata['NTRP']
        self.untrp = pdata['microNTRP']
        self.name = self.first + " " + self.last
        
    def Name(self):
        return self.name

    def __repr__(self):
        return "%s %4.2f (%4.2f)" % (self.name,self.ntrp,self.untrp)
        

