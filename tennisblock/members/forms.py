
from django import forms
from tennisblock.blockdb.models import Player

class PlayerForm(forms.ModelForm):
    fields = [
        'first',
        'last',
        'gender',
        'ntrp',
        'microntrp',
        'email',
        'phone'
    ]
    class Meta:
        model = Player
        #exclude = ('created_by',)
