from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from blockdb.models import Couple, SeasonPlayer


class CoupleForm(ModelForm):

    def __init__(self, season, *args, **kwargs):
        super(CoupleForm, self).__init__(*args, **kwargs)
        allPlayers = SeasonPlayer.objects.filter(season=season)
        couples = Couple.objects.filter(season=season)
        self.fields['male'].queryset = \
            allPlayers.filter(player__gender='M')\
            .exclude(player__id__in=couples.values('male'))
        self.fields['female'].queryset = allPlayers.filter(player__gender='F') \
            .exclude(player__id__in=couples.values('female'))

    def is_valid(self):
        if self.data['name'] == "":
            return False

        try:
            self.spguy = SeasonPlayer.objects.get(pk=self.data['male'])
            self.spgal = SeasonPlayer.objects.get(pk=self.data['female'])
        except ObjectDoesNotExist:
            return False

        return True

    class Meta:
        model = Couple
        fields = ['name', 'male', 'female', 'fulltime',
                  'blockcouple', 'canschedule']


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             required=True,
                             label=_('Please enter your e-mail address.'),
                             widget=forms.EmailInput({
                                 'id': 'bootstrap-email',
                             }))
    message = forms.CharField(max_length=500,
                              required=True,
                              label=_('Enter your message'),
                              widget=forms.Textarea({
                                  'id': 'bootstrap-message',
                                  'cols': '60', 'rows': '10'})
                              )


class AvailabilityForm(forms.Form):
    name = forms.CharField(label=_('Player name'), )
    # availability = forms.BooleanField(required=False)
