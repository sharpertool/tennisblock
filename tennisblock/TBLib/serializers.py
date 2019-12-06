
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from blockdb.models import Player, Schedule


class PlayerSerializer(ModelSerializer):
    name = serializers.CharField(source='full_name')
    untrp = serializers.FloatField(source='microntrp')

    class Meta:
        model = Player
        fields = ['id', 'name', 'ntrp', 'untrp', 'gender']
