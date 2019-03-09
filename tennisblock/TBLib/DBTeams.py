from blockdb.models import Matchup, Schedule, Player
from api.apiutils import get_meeting_for_date


class DBTeams:
    def __init__(self):
        self.meeting = None

    def get_meeting(self, date=None):
        """
        Return the cached matchid, or get a new one.
        """
        if self.meeting:
            return self.meeting

        m = get_meeting_for_date(date)
        self.meeting = m
        return m

    def get_players(self, date=None):

        m = self.get_meeting(date)

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
                raise Exception("No proper Gender!")

        return men, women

    def init_teamgen(self):
        """
        Remove all of the slots for the given date.
        """
        Matchup.objects.filter(meeting=self.get_meeting()).delete()

    def delete_matchup(self, date):
        """
        Delete the matchup for the given date.
        """
        meeting = self.get_meeting(date)
        if meeting:
            Matchup.objects.filter(meeting=meeting).delete()

    def insert_records(self, date, seq):
        """
        Insert the sequence
        """

        meeting = self.get_meeting(date)
        self.delete_matchup(meeting)

        # Insert the slots
        set = 1
        for s in seq:
            court = 1
            for m in s.matches:
                t1_p1 = Player.objects.get(pk=m.t1.p1.pk)
                t1_p2 = Player.objects.get(pk=m.t1.p2.pk)
                t2_p1 = Player.objects.get(pk=m.t2.p1.pk)
                t2_p2 = Player.objects.get(pk=m.t2.p2.pk)
                matchup = Matchup.objects.create(
                        meeting=meeting,
                        set=set,
                        court=court,
                        team1_p1=t1_p1,
                        team1_p2=t1_p2,
                        team2_p1=t2_p1,
                        team2_p2=t2_p2
                )
                matchup.save()

                court += 1

            set += 1

    def query_match(self, date):
        """
        Query all of the records for the given date.
        """

        def serializeTeam(p1, p2):
            return {
                'm': {
                    'name': p1.Name(),
                    'ntrp': p1.ntrp,
                    'untrp': p1.microntrp,
                },
                'f': {
                    'name': p2.Name(),
                    'ntrp': p2.ntrp,
                    'untrp': p2.microntrp,
                }
            }

        meeting = self.get_meeting(date)

        matchups = Matchup.objects.order_by('set', 'court').filter(meeting=meeting)

        if len(matchups) == 0:
            return None

        data = []

        currSet = 1
        courtArray = []
        for matchup in matchups:
            if currSet != matchup.set:
                data.append(courtArray)
                courtArray = []
                currSet = matchup.set

            matchData = {
                'team1': serializeTeam(matchup.team1_p1, matchup.team1_p2),
                'team2': serializeTeam(matchup.team2_p1, matchup.team2_p2)
            }
            courtArray.append(matchData)

        data.append(courtArray)  # Don't forget the last one!

        return data
