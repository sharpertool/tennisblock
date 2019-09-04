from django import forms
from django.utils.translation import ugettext_lazy as _

class AvailabilityForm(forms.Form):
    name = forms.CharField(label=_('Player name'), )
    # availability = forms.BooleanField(required=False)
