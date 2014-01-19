
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _


from tennisblock.blockdb.models import Couple,SeasonPlayers

class CoupleForm(ModelForm):

    def __init__(self,season,*args,**kwargs):
        super (CoupleForm,self).__init__(*args,**kwargs)
        allPlayers = SeasonPlayers.objects.filter(season=season)
        self.fields['male'].queryset = allPlayers.filter(player__gender='M')
        self.fields['female'].queryset = allPlayers.filter(player__gender='F')

    def is_valid(self):
        if self.data['name'] == "":
            return False

        try:
            self.spguy = SeasonPlayers.objects.get(pk=self.data['male'])
            self.spgal = SeasonPlayers.objects.get(pk=self.data['female'])
        except ObjectDoesNotExist:
            return False

        return True

    class Meta:
        model= Couple
        fields=['name','male','female','fulltime','blockcouple']


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             required=True,
                             label=_('Please enter your e-mail address.'),
                             widget=forms.TextInput({
                                 'id': 'bootstrap-email',
                                 }))
    message = forms.CharField(max_length=500,
                              required=True,
                              label=_('Enter your message'),
                              widget=forms.Textarea({
                                  'id':'bootstrap-message',
                                  'cols': '60', 'rows': '10'})
    )

