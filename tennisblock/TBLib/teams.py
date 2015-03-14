
#!/usr/bin/env python

from teamgen.TeamGen2 import TeamGen
from teamgen.DBTeams import DBTeams


class TeamManager(object):

    def __init__(self, matchid = None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def pickTeams(self,date=None,**kwargs):

        men,women = self.dbTeams.getPlayers(date)

        assert(len(men) == len(women))

        isTesting = kwargs.get('test',True)
        noDupes = kwargs.get('nodupes',False)

        # Calculate number fo courts based on # of men.
        # Assume # of women is the same.
        nCourts = kwargs.get('courts', len(men)/2)
        nSequences = kwargs.get('sequences',3)


        if len(men) < nCourts*2 or len(women) < nCourts*2:
            errmsg = "Cannot pick teams, there are not enough men or women."
            errmsg += "Need %d of both. Have %d men and %d women." % (nCourts*2,len(men),len(women))
            return {"status" : {"error" : errmsg}}

        tg = TeamGen(nCourts,nSequences,men,women)
        sequences = tg.generate_set_sequences(noDupes)

        if sequences == None or len(sequences) < nSequences:
            return {"status" : {"error" : "Could not generate the required sequences"}}

        else:
            # Put the worst sequences last.
            sequences.reverse()
            tg.display_sequences(sequences)
            tg.show_all_diffs(sequences)

            if not isTesting:
                self.dbTeams.InsertRecords(date,sequences)

            return sequences

    def queryMatch(self,date=None):

        matchdata = self.dbTeams.queryMatch(date)
        return matchdata

def main():

    # Do some testing
    pass

if __name__ == '__main__':
    main()
