from django import forms
from crispy_forms.helper import FormHelper
from blockdb.models import Season


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('name', 'courts', 'firstcourt',
                  'startdate', 'enddate',
                  'blockstart', 'lastdate', 'blocktime')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'


