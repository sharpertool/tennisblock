from django import forms
from django.utils.translation import ugettext_lazy as _


class NotifyForm(forms.Form):
    message = forms.CharField(max_length=500,
                              required=True,
                              label=_('Enter your message'),
                              widget=forms.Textarea({
                                  'id':'bootstrap-message',
                                  'cols': '60', 'rows': '10'})
    )

