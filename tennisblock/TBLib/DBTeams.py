from django.core.exceptions import ObjectDoesNotExist

from blockdb.models import Matchup, Schedule, Player, Meeting
from api.apiutils import get_meeting_for_date
from teamgen.meeting_history import MeetingHistory
from teamgen import Player as TPlayer, MatchRound, Match, Team


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

    def delete_match(self, date, set_number):
        """
        Delete the matchup for the given date.
        """
        meeting = self.get_meeting(date)
        if meeting:
            Matchup.objects.filter(meeting=meeting, set=set_number).delete()

    def insert_generated_sequence(self, date, seq):

        meeting = self.get_meeting(date)
        self.delete_matchup(meeting)

        for set_idx, s in enumerate(seq):
            for court_idx, m in enumerate(s):
                t1_p1 = Player.objects.get(pk=m.get('t1').get('p1').get('pk'))
                t1_p2 = Player.objects.get(pk=m.get('t1').get('p2').get('pk'))
                t2_p1 = Player.objects.get(pk=m.get('t2').get('p1').get('pk'))
                t2_p2 = Player.objects.get(pk=m.get('t2').get('p2').get('pk'))
                match_up = Matchup.objects.create(
                        meeting=meeting,
                        set=set_idx+1,
                        court=court_idx+1,
                        team1_p1=t1_p1,
                        team1_p2=t1_p2,
                        team2_p1=t2_p1,
                        team2_p2=t2_p2
                )
                match_up.save()

    def get_current_sequence(self, date):
        """
        A match looks like this

                {
            "t1": {
                "p1": {
                    "pk": 135,
                    "gender": "M",
                    "ntrp": 4.0,
                    "microntrp": 4.15,
                    "phone": "(208) 353-8808",
                    "name": "Jeff Thompson"
                },
                "p2": {
                    "pk": 149,
                    "gender": "F",
                    "ntrp": 3.5,
                    "microntrp": 3.8,
                    "phone": "(208) 869-2133",
                    "name": "Patty ONeill"
                }
            },
            "t2": {
                "p1": {
                    "pk": 150,
                    "gender": "M",
                    "ntrp": 3.5,
                    "microntrp": 3.5,
                    "phone": "(208) 830-9913",
                    "name": "Derrick ONeill"
                },
                "p2": {
                    "pk": 7,
                    "gender": "F",
                    "ntrp": 4.0,
                    "microntrp": 4.2,
                    "phone": "(208) 672-9254",
                    "name": "Jenny Grunke"
                }
            }
        },

        :param date:
        :return:
        """

        meeting = self.get_meeting(date)

        matchups = Matchup.objects.filter(meeting=meeting).order_by('set', 'court')

        from django.db.models import Max
        sets = Matchup.objects.filter(meeting=meeting).aggregate(Max('set'))['set__max']
        courts = Matchup.objects.filter(meeting=meeting).aggregate(Max('court'))['court__max']

        # Assume 3 sets
        sequences = []
        for x in range(sets):
            sequences.append([])
            for y in range(courts):
                sequences[x].append({})

        for matchup in matchups:
            match = sequences[matchup.set-1][matchup.court-1]

            pass


        return sequences

    def insert_records(self, date, seq):
        """
        Insert the sequence
        """

        meeting = self.get_meeting(date)
        self.delete_matchup(meeting)

        for set_idx, s in enumerate(seq):
            for court_idx, m in enumerate(s.matches):
                t1_p1 = Player.objects.get(pk=m.t1.p1.pk)
                t1_p2 = Player.objects.get(pk=m.t1.p2.pk)
                t2_p1 = Player.objects.get(pk=m.t2.p1.pk)
                t2_p2 = Player.objects.get(pk=m.t2.p2.pk)
                match_up = Matchup.objects.create(
                        meeting=meeting,
                        set=set_idx+1,
                        court=court_idx+1,
                        team1_p1=t1_p1,
                        team1_p2=t1_p2,
                        team2_p1=t2_p1,
                        team2_p2=t2_p2
                )
                match_up.save()

    def query_match(self, date):
        """
        Query all of the records for the given date.
        """

        def serialize_team(p1, p2):
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
                'team1': serialize_team(matchup.team1_p1, matchup.team1_p2),
                'team2': serialize_team(matchup.team2_p1, matchup.team2_p2)
            }
            courtArray.append(matchData)

        data.append(courtArray)  # Don't forget the last one!

        return data

    def get_history(self, date=None, sets=None):
        """
        Build a history for the given date and sets.

        If sets is None, use all. If sets is an array of values,
        used only history data for those sets. This allows the history
        to be used to build or re-build a particular set
        :param date:
        :param sets:
        :return:
        """

        meeting = self.get_meeting(date)
        matchups = Matchup.objects.filter(meeting=meeting)
        if sets is None:
            sets = Matchup.objects.filter(meeting=meeting).values_list('set', flat=True)

        rounds = []
        group1 = []
        group2 = []
        history = MeetingHistory(group1, group2)
        for set in sorted(sets):
            matches = matchups.filter(set=set).select_related('team1_p1', 'team1_p2', 'team2_p1', 'team2_p2')
            round = MatchRound()

            for match in matches:
                print(match.court)
                group1.extend([match.team1_p1, match.team2_p1])
                group2.extend([match.team1_p2, match.team2_p2])
                m = Match(Team(match.team1_p1, match.team1_p2), Team(match.team2_p1, match.team2_p2))
                round.add_match(m)

            rounds.append(round)
            history.add_round(round)

        return history








