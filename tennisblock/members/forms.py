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


class PlayerUserForm(forms.ModelForm):
    first = forms.CharField(max_length=40, required=True)
    last = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=False)
    gender = forms.ChoiceField(choices=Player.GENDER_CHOICES, required=True)
    ntrp = forms.FloatField(required=True)
    microntrp = forms.FloatField(required=False)
    phone = forms.CharField(max_length=14, required=False)

    class Meta:
        model = Player
        fields = ('first', 'last', 'email', 'gender', 'ntrp', 'microntrp', 'phone')
