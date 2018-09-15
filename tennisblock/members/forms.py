from django import forms
from blockdb.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'gender',
            'ntrp',
            'microntrp',
            'phone'
        ]
