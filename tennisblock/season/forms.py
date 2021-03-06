from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from blockdb.models import Season, Couple, SeasonPlayer


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = ('name', 'courts', 'firstcourt',
                  'startdate', 'enddate',
                  'blockstart', 'lastdate', 'blocktime')
        widgets = {
            'startdate': DatePickerInput(format='%m/%d/%Y'),
            'enddate': DatePickerInput(format='%m/%d/%Y'),
            'blockstart': DatePickerInput(format='%m/%d/%Y'),
            'lastdate': DatePickerInput(format='%m/%d/%Y'),
            'blocktime': TimePickerInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'


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