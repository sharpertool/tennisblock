
from django import forms
from tennisblock.blockdb.models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        #exclude = ('created_by',)
