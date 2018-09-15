from textwrap import dedent

from django.views.generic import TemplateView
from django.core.mail import send_mail

from django.forms.formsets import (
    formset_factory, BaseFormSet)

from django import forms
from django.shortcuts import render
from django.conf import settings

from TBLib.view import TennisLoginView
from blockdb.models import Season, Couple, SeasonPlayer
from .forms import ContactForm

from .forms import CoupleForm, AvailabilityForm
from TBLib.view import class_login_required


class HomeView(TemplateView):
    template_name = "home.html"


@class_login_required
class AvailabilityView(TemplateView):
    template_name = "availability.html"


class AvailabilityFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(AvailabilityFormSet, self).add_fields(form, index)
        form.field_list = []
        for x in xrange(12):
            f = forms.BooleanField(required=False, label='')
            field_nm = "avail_{}".format(x)
            form.fields[field_nm] = f
            form.field_list.append(field_nm)


@class_login_required
class AvailabilityFormView(TemplateView):
    template_name = "availability_form.html"
    thankyou_template = "thankyou.html"

    def _get_formset(self, data=None):
        """ Create the formset object """
        fs = formset_factory(AvailabilityForm, extra=31, formset=AvailabilityFormSet)
        initial_data = [{'name': 'Billy Bob'}]
        if data:
            return fs(data=data, initial=initial_data)
        return fs(initial=initial_data)

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['formset'] = self._get_formset()

        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_context_data()
        fs = self._get_formset(data=request.POST)

        if fs.is_valid():
            print("Valid Formset!")

            return render(request,
                          self.thankyou_template,
                          context)
        else:
            print("Form is invalid")
            context['formset'] = fs
            return render(request, self.template_name, context)


@class_login_required
class PlaysheetView(TennisLoginView):
    template_name = "playsheet.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"
    thankyou_template = "thankyou.html"

    def get(self, request):
        form = ContactForm()
        return render(request,
                      self.template_name,
                      {'form': form}
                      )

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            from_email = settings.EMAIL_HOST_USER
            recipient_list = settings.CONTACT_FORM_RECIPIENTS

            sender_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            message = "FROM: %s\n\n\nMESSAGE:\n\n%s" % (sender_email, message)

            subject = settings.CONTACT_FORM_SUBJECT

            send_mail(subject, message, from_email, recipient_list)

            return render(request,
                          self.thankyou_template,
                          {'form': form})

        return render(request,
                      self.template_name,
                      {'form': form})


@class_login_required
class CouplesView(TemplateView):
    template_name = "couple_editor.html"

    def get_context_data(self, **kwargs):
        context = super(CouplesView, self).get_context_data(**kwargs)
        return context

    def getcurentcouples(self, context, season):
        players = SeasonPlayer.objects.filter(season=season)
        couples = Couple.objects.filter(season=season)

        context['players'] = players
        context['couples'] = couples
        initial = {
            'season': season.pk,
            'fulltime': False,
            'blockcouple': True,
            'canschedule': True
        }
        context['form'] = CoupleForm(season, initial=initial)

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.filter(pk=pk)
            if s.count():
                season = s[0]
                context['season'] = season

                self.getcurentcouples(context, season)

        return self.render_to_response(context)

    def post(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            s = Season.objects.get(pk=pk)
            context['season'] = s

            form = CoupleForm(s, request.POST)
            if form.is_valid():
                print("Valid Couple form..updating...")
                Couple.objects.create(
                    season=s,
                    name=form.data['name'],
                    male=form.spguy.player,
                    female=form.spgal.player,
                    fulltime=form.data.get('fulltime', 'off') == 'on',
                    blockcouple=form.data.get('blockcouple', 'off') == 'on',
                    canschedule=True
                ).save()
                print("Inserted couple")
                context['form'] = CoupleForm(s)
            else:
                print("Invalid Couple")
                context['form'] = form

            self.getcurentcouples(context, s)
            return self.render_to_response(context)
        except:
            return self.render_to_response(context)
