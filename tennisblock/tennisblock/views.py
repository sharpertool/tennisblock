# Create your views here.

from TBLib.view import TennisView,TennisLoginView
from blockdb.models import Season,Meetings,Couple,Player,SeasonPlayers
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from forms import ContactForm

from .forms import CoupleForm,NotifyForm
from TBLib.schedule import Scheduler
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

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
        context['form'] = CoupleForm(season)

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

class ScheduleNotify(TennisView):
    template_name = "schedule_notify.html"
    thankyou_template = "thankyou.html"

    def getCouples(self,sch):

        import random
        couples = []
        gals = sch.get('gals')
        guys = sch.get('guys')

        for x in range(0,len(gals)):
            couple = [gals[x].get('name'),guys[x].get('name')]
            random.shuffle(couple)
            couples.append(couple)

        return couples

    def generateNotifyMessage(self,date,players,extramsg):
        """
        Generate plain text version of message.
        """

        couples = self.getCouples(players)
        cstrings = ["%s and %s" % (c[0],c[1]) for c in couples]
        prefix = "      - "
        msg = """

Here is the schedule for Friday, %s:

%s

%s

        """ % (date,extramsg,prefix + prefix.join(cstrings))

        return msg

    def generateHtmlNotifyMessage(self,date,players,extramsg):
        """
        Generate an HTML Formatted version of the message.
        """

        couples = self.getCouples(players)
        cstrings = ["<li><span>%s</span> and <span>%s</span></li>"
                    % (c[0],c[1]) for c in couples]

        msg = """

        <html>
        <head></head>
        <body>
            <h3>Here is the schedule for Friday, %s:</h3>

        %s

        <ul>
            %s
        </ul>

        """ % (date,extramsg,"\n".join(cstrings))

        return msg

    def get_context_data(self,**kwargs):

        context = super(ScheduleNotify,self).get_context_data(**kwargs)

        date =kwargs.get('date')

        tb = Scheduler()
        if settings.BLOCK_NOTIFY_RECIPIENTS:
            recipient_list = ['ed@tennisblock.com','viquee@me.com']
        else:
            recipient_list = tb.getBlockEmailList()

        schedule = tb.querySchedule(date)
        context['couples'] = self.getCouples(schedule)
        context['date'] = date

        context['recipients'] = recipient_list
        return context

    def get(self, request,date):
        context = self.get_context_data(date=date)
        form = NotifyForm()

        context['form'] = form

        return render(request,
                      self.template_name,
                      context
        )

    def post(self, request,date):

        form = NotifyForm(request.POST)

        if form.is_valid():

            extramsg = form.cleaned_data['message']

            tb = Scheduler()

            players = tb.querySchedule(date)

            from_email = settings.EMAIL_HOST_USER

            # Generate Text and HTML versions.
            message = self.generateNotifyMessage(date,players,extramsg)
            html = self.generateHtmlNotifyMessage(date,players,extramsg)

            subject = settings.BLOCK_NOTIFY_SUBJECT % date

            if settings.BLOCK_NOTIFY_RECIPIENTS:
                recipient_list = ['ed@tennisblock.com','viquee@me.com']
            else:
                recipient_list = tb.getBlockEmailList()

            msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            msg.attach_alternative(html,'text/html')

            msg.send()

            return render(request,
                          self.thankyou_template,
                          {'form': form})

        return render(request,
                      self.template_name,
                      {'form': form})


