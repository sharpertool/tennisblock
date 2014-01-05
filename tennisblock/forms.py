
from django.forms import ModelForm,Form,CharField,ModelChoiceField,BooleanField,ChoiceField,Select
from django.core.exceptions import ObjectDoesNotExist

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



