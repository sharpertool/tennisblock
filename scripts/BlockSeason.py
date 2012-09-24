#!/usr/bin/env python

import argparse

import os
import openpyxl

from DBTennisBlock import DBTennisBlock
from DBBlockSeason import DBBlockSeason

class BlockSeason(object):

    def __init__(self,conn):

        self.conn = conn

        self.isxlsx = False

        self.initDatabaseConnections()


    def initDatabaseConnections(self):

        self.dbseason = DBBlockSeason(self.conn)
        self.dbblock = DBTennisBlock(self.conn)

    def getSheet(self,wb,name):

        if self.isxlsx:
            ws = wb.get_sheet_by_name(name)
        else:
            ws = wb.sheet_by_name(name)

        return ws

    def getValues(self,ws,row,cols=None):

        if self.isxlsx:
            wsrow = ws.rows[row]
            values = []
            for cell in wsrow:
                val = cell.value
                if val == None:
                    val = ''
                values.append(val)
            return values
        else:
            return ws.row_values(row)

    def getRowCount(self,ws):

        if self.isxlsx:
            return ws.get_highest_row()
        else:
            return ws.nrows

    def getPlayers(self,ws):
        """
        Retrieve the players from the worksheet
        """
        nrows = self.getRowCount(ws)
        rowHeadings = self.getValues(ws,0)

        players = []

        for rowid in range(1,nrows):
            theRow = self.getValues(ws,rowid)
            player = dict(zip(rowHeadings, theRow))
            if not player['First'] == "" and not player['Last'] == "":
                players.append(player)
            else:
                pass

        return players

    def getMeetings(self,ws):
        """
        Return the list of meetings and info about them.
        """

        nrows = self.getRowCount(ws)
        rowHeadings = self.getValues(ws,0)

        meetings = []

        for rowid in range(1,nrows):
            theRow = self.getValues(ws,rowid)
            meeting = dict(zip(rowHeadings, theRow))
            if not meeting['date'] == "" and not meeting['holdout'] == "":
                meetings.append(meeting)
            else:
                pass

        return meetings

    def getPlayerId(self,p):

        if p['PID'] != None:
            return p['PID']

        pid = self.dbblock.getPlayerId(p['First'],p['Last'])
        return pid

    def getCouples(self,players):
        """
        Find players with the same Couplename
        """

        couples = {}

        for p in players:
            cname = p['Couplename']
            pid = self.getPlayerId(p)
            if not couples.has_key(cname):
                couples[cname] = {
                    'pa_id' : None,
                    'pb_id' : None,
                    'fulltime' : 0,
                    'canschedule' : 1,
                    'blockcouple' : 1,
                }
            c = couples[cname]
            c['fulltime'] = p['FullTime']
            if p['Gender'] == 'm':
                c['pa_id'] = pid
            else:
                c['pb_id'] = pid

        return couples

    def importExcel(self,xlfile):
        """
        Import the excel file that contains season information

        """

        print("Importing Excel Season file %s" % xlfile)

        theFile = os.path.expanduser(xlfile)

        try:
            (root,ext) = os.path.splitext(theFile)
            if ext == '.xlsx':
                self.isxlsx = True
                wb = openpyxl.load_workbook(theFile)
                self.sheets = wb.get_sheet_names()
            else:
                self.isxlsx = False
                wb = xlrd.open_workbook(theFile)

        except Exception as e:
            print("Excel Read module could not open the file %s" % theFile)
            return

        wsPlayers = self.getSheet(wb,'Players')
        if wsPlayers == None:
            print("Players worksheet not found in %s" % theFile)

        wsMeetings = self.getSheet(wb,'Meetings')
        if wsMeetings == None:
            print("Meetings worksheet not found in %s" % theFile)

        players = self.getPlayers(wsPlayers)
        meetings = self.getMeetings(wsMeetings)

        return players,meetings


    def newSeason(self,xlfile,season,courts,firstCourt):

        players,meetings = self.importExcel(xlfile)

        if players and meetings:
            sid = self.dbblock.getSeasonId(season)
            if not sid:
                sid = self.dbblock.insertSeason(season,courts,firstCourt)

            self.dbblock.clearSeason(season)
            self.dbblock.addMeetings(season,meetings)
            self.dbblock.addPlayers(season,players)
            couples = self.getCouples(players)
            self.dbblock.addCouples(season,couples)


def main():

    pass



if __name__ == '__main__':
    main()


    
    
    

