from django import forms
from django.utils.translation import ugettext_lazy as _


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
