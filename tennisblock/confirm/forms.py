from django import forms
from django.utils.translation import ugettext_lazy as _


class ScheduleRejectForm(forms.Form):

    reason = forms.CharField(max_length=500,
                              required=False,
                              label=_('Reason for Rejecting Schedule'),
                              widget=forms.Textarea({
                                  'id':'bootstrap-message',
                                  'cols': '60', 'rows': '10'})
    )

