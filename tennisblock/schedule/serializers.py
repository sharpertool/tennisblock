__author__ = 'kutenai'

from blockdb.models import Meetings

from rest_framework import serializers

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meetings
        fields=('date', 'holdout', 'id')