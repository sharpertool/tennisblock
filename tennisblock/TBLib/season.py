__author__ = 'kutenai'
import datetime

from blockdb.models import Season, Meetings

class SeasonManager(object):
    """
    Manage season information and calculate season related values.
    """

    def __init__(self, season=None):

        self.season = season or self.get_current_season()
        if not self.season:
            raise Exception("Could not determine the current season.")

    def get_current_season(self, season=None):
        """
        Return the current season object.
        """

        seasons = Season.objects.order_by('startdate').filter(lastdate__gte=datetime.date.today())
        if seasons.count() > 0:
            season = seasons[0]

            meetings = Meetings.objects.filter(
                    season=season,
                    holdout=False,
                    date__gte=datetime.date.today())

            if meetings.count() > 0:
                return season

            # If we are past the last date of the current block season, return
            # the next season if there is one.
            if seasons.count() > 1:
                return seasons[1]

        return None

    def get_meeting_list(self, holdouts=False):
        """
        Get a list of meetings for this season.

        """

        meetings = Meetings.objects.filter(season=self.season).order_by('date')
        if not holdouts:
            meetings = meetings.filter(holdout=False)

        return meetings





