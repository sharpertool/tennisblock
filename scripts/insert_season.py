#!/usr/bin/env python

import MySQLdb
from MySQLdb import *
import os
import time
import datetime
import sys

from DBManager import DBSeason

currSeason = {
    'name' : "2012 Spring",
    'courts' : [9,10,11,12]
}

couples = {
    "Henderson" : {
        'm':        "Ed Henderson",
        'f':        "Vicki Henderson",
        'split':    'Full'
    },
    "Bloomers" : {
        'm':        "Jonathan Bloomer",
        'f':        "Linda Bloomer",
        'split':    'Half'
    },
    "Grunkes" : {
        'm':        "James Grunke",
        'f':        "Jenny Grunke",
        'split':    'Half'
    },
    "Bettis" : {
        'm':        "Dave Bettis",
        'f':        "Lisa Bettis",
        'split':    'Half'
    },
    "Pearces" : {
        'm':        "John Pearce",
        'f':        "Corie Pearce",
        'split':    'Half'
    },
    "Jake & Janice" : {
        'm':        "Jake Putnam",
        'f':        "Janice Ehrhart",
        'split':    'Half'
    },
    "Robb & Ronna" : {
        'm':        "Robb Child",
        'f':        "Ronna Parish-Child",
        'split':    'Half'
    },
    "Rod & Joanne" : {
        'm':        "Rod Kimerling",
        'f':        "Joanne Koplin",
        'split':    'Half'
    },
    "Smiths" : {
        'm':        "Mark Smith",
        'f':        "Debbie Smith",
        'split':    'Half'
    },
    "Braithwaites" : {
        'm':        "Rita Braithwaite",
        'f':        "Richard Braithwaite",
        'split':    'Half'
    },
    "Kirk & Tina" : {
        'm':        "Tina Measham",
        'f':        "Kirk Whitaker",
        'split':    'Half'
    },
    "Trasks" : {
        'm':        "Jeff Trask",
        'f':        "Sonja Trask",
        'split':    'Half'
    },
    "Kirk & Tina" : {
        'm':        "Tina Measham",
        'f':        "Kirk Whitaker",
        'split':    'Half'
    },
    "Ken & Lisa" : {
        'm':        "Ken Cross",
        'f':        "Lisa Dekerchove",
        'split':    'Half'
    },
    "John & Carla" : {
        'm':        "John Morenzi",
        'f':        "Carla Latta",
        'split':    'Half'
    },
    "Powells" : {
        'm':        "Tim Powell",
        'f':        "Jan Powell",
        'split':    'Half'
    },
}

blockStartDate = '2012/01/13'
blockEndDate = '2012/04/20'

blockHoldouts = ['2012/01/13','2012/02/17','2012/04/20']

def main():

    season = DBSeason(currSeason,blockStartDate, blockEndDate, blockHoldouts)

    bAllGood = season.verifyPlayers(couples)

    if not bAllGood:
        print("Some Player names have issues..")
        sys.exit()

    season.insertCouples(couples)

    season.insertBlockMeetings()


if __name__ == '__main__':
    main()

