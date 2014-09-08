
from django import forms
from blockdb.models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'first',
            'last',
            'gender',
            'ntrp',
            'microntrp',
            'email',
            'phone'
        ]
