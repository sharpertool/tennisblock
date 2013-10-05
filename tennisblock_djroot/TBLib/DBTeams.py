
import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings.dev'

from django.db import connection
from blockdb.models import Team,Matchup,Schedule
from api.apiutils import _getMeetingForDate

class DBTeams(object):

    def __init__(self):
        self.meeting = None

    def getMeeting(self,date=None):
        """
        Return the cached matchid, or get a new one.
        """
        if self.meeting:
            return self.meeting

        m = _getMeetingForDate(date)
        self.meeting = m
        return m

    def getPlayers(self,date=None):

        m = self.getMeeting(date)

        men = []
        women = []

        sched = Schedule.objects.filter(meeting=m)
        for s in sched:
            p = s.player
            if p.gender == 'F':
                women.append(p)
            elif p.gender == 'M':
                men.append(p)
            else:
                raise("No proper Gender!")

        return men,women

    def initTeamGen(self):
        """
        Remove all of the slots for the given date.
        """
        Matchup.objects.filter(meeting = self.getMeeting()).delete()
        pass

    def InsertRecords(self,date,seq):
        """
        Insert the sequence
        """

        self.initTeamGen()

        meeting = self.getMeeting(date)

        # Insert the slots

        set = 1
        for s in seq:
            court = 1
            for m in s.matches:

                t1 = Team.objects.create(
                    male    = m.t1.m,
                    female  = m.t1.f
                )
                t2 = Team.objects.create(
                    male    = m.t2.m,
                    female  = m.t2.f
                )

                matchup = Matchup.objects.create(
                    meeting     = meeting,
                    set         = set,
                    court       = court,
                    team1       = t1,
                    team2       = t2
                )
                matchup.save()

                court += 1

            set += 1


    def queryMatch(self,date):
        """
        Query all of the records for the given date.
        """

        def serializeTeam(team):
            return {
                'm' : {
                    'name' : team.male.Name(),
                    'ntrp' : team.male.ntrp,
                    'untrp': team.male.microntrp,
                    },
                'f' : {
                    'name' : team.female.Name(),
                    'ntrp' : team.female.ntrp,
                    'untrp': team.female.microntrp,
                    }
            }


        meeting = self.getMeeting(date)

        matchups = Matchup.objects.order_by('set','court').filter(meeting=meeting)


        if len(matchups) == 0:
            return None


        data = []

        currSet = 1
        currCourt = 1
        courtArray = []
        for matchup in matchups:
            if currSet != matchup.set:
                data.append(courtArray)
                courtArray = []
                currSet = matchup.set

            matchData = {
                'team1' : serializeTeam(matchup.team1),
                'team2' : serializeTeam(matchup.team2)
            }
            courtArray.append(matchData)

        data.append(courtArray) # Don't forget the last one!

        return data










def main():

    pass


if __name__ == '__main__':
    main()


