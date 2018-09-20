from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from blockdb.models import Player


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'gender',
            'ntrp',
            'microntrp',
            'phone'
        ]


