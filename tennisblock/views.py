# Create your views here.

from tennisblock.TBLib.view import TennisView,TennisLoginView
from tennisblock.blockdb.models import Season,Meetings,Couple,Player,SeasonPlayers
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from forms import ContactForm

from .forms import CoupleForm

class HomeView(TennisView):
    template_name = "home.html"

class BlockSchedule(TennisLoginView):
    template_name = "schedule.html"

class AvailabilityView(TennisLoginView):
    template_name = "availability.html"

class PlaysheetView(TennisLoginView):
    template_name = "playsheet.html"

class AboutView(TennisView):
    template_name = "about.html"

class ContactView(TennisView):
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

class SeasonsView(TennisLoginView):
    template_name = "seasons.html"

    #queryset = Season.objects.all()

    def get_context_data(self,**kwargs):
        context = super(SeasonsView,self).get_context_data(**kwargs)
        context['seasons'] = Season.objects.all()

        return context

    def get(self,request,pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.filter(pk=pk)
            if s.count():
                context['season'] = s[0]

                context['meetings'] = Meetings.objects.filter(season=s)

        return self.render_to_response(context)


class CouplesView(TennisLoginView):
    template_name = "couple_editor.html"

    def get_context_data(self,**kwargs):
        context = super(CouplesView,self).get_context_data(**kwargs)
        return context

    def getcurentcouples(self,context,season):
        players = SeasonPlayers.objects.filter(season=season)
        couples = Couple.objects.filter(season=season)

        context['players'] = players
        context['couples'] = couples
        context['form']   = CoupleForm(season)

    def get(self,request,pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.filter(pk=pk)
            if s.count():
                season = s[0]
                context['season'] = season

                self.getcurentcouples(context,season)


        return self.render_to_response(context)

    def post(self,request,pk=None, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            s = Season.objects.get(pk=pk)
            context['season'] = s

            form = CoupleForm(s,request.POST)
            if form.is_valid():
                print("Valid Couple form..updating...")
                Couple.objects.create(
                    season=s,
                    name=form.data['name'],
                    male = form.spguy.player,
                    female = form.spgal.player,
                    fulltime = form.data.get('fulltime','off') == 'on',
                    blockcouple = form.data.get('blockcouple','off') == 'on',
                    canschedule=True
                ).save()
                print("Inserted couple")
                context['form'] = CoupleForm(s)
            else:
                print("Invalid Couple")
                context['form'] = form

            self.getcurentcouples(context,s)
            return self.render_to_response(context)
        except:
            return self.render_to_response(context)
