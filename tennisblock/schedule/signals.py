import django.dispatch
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

player_confirmed = django.dispatch.Signal(providing_args=["player", "request"])
player_rejected = django.dispatch.Signal(providing_args=["player", "request"])


def onPlayerConfirmed(sender=None, player=None, request=None, **kwargs):
    print('onPlayerConfirmed called')
    message = f"Player {player} has confirmed"

    subject = f"Player {player} Confirmed"

    recipient_list = ['ed@tennisblock.com']
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)

    msg.send()
    print(f"Confirmed for {player}")


def onPlayerRejected(sender=None, player=None, request=None, **kwargs):
    print('onPlayerRejected called')
    message = f"Player {player} has rejected"

    subject = f"Player {player} Confirmed"


    recipient_list = ['ed@tennisblock.com']
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)

    msg.send()
    print(f"Rejected for {player}")


player_confirmed.connect(onPlayerConfirmed)
player_confirmed.connect(onPlayerRejected)