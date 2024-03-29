import django.dispatch
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from tennis_channels.sync_handlers import ScheduleSyncHandler

player_confirmed = django.dispatch.Signal(providing_args=["player", "request"])
player_rejected = django.dispatch.Signal(providing_args=["player", "reason", "request"])


def send_verify_email_to_captains(confirmed=True, player=None, reason=None):
    name = player.get_full_name()
    if confirmed:
        message = f"{name} has confirmed"
        subject = f"{name} Confirmed Schedule"
    else:
        message = f"{name} has rejected.\nReason is:\n{reason}"
        subject = f"{name} Rejected Schedule7"

    recipient_list = ['ed@tennisblock.com']
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)

    msg.send()


def on_player_confirmed(sender=None, player=None, request=None, **kwargs):
    print('on_player_confirmed called')
    send_verify_email_to_captains(confirmed=True, player=player)

    date = sender.schedule.meeting.date
    sdate = date.strftime("%Y-%m-%d")
    pdata = {
        'user_id': player.id,
        'name': player.full_name
    }
    ScheduleSyncHandler.schedule_verify_update(schedule_date=sdate,
                                               player=pdata)


def on_player_rejected(sender=None, player=None, reason=None, request=None, **kwargs):
    print('on_player_rejected called')
    send_verify_email_to_captains(confirmed=False, player=player, reason=reason)

    date = sender.schedule.meeting.date
    sdate = date.strftime("%Y-%m-%d")
    pdata = {
        'user_id': player.id,
        'name': player.full_name
    }
    ScheduleSyncHandler.schedule_verify_update(schedule_date=sdate,
                                               status=False,
                                               player=pdata,
                                               msg=reason)


player_confirmed.connect(on_player_confirmed)
player_rejected.connect(on_player_rejected)
