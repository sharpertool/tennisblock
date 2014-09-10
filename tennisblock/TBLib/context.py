from __future__ import absolute_import

from os.path import join

from django.conf import settings


def tennisblock(request):
    return {
        'angularapp': 'tennisblock',
        'isLoggedIn': request.user.is_authenticated(),
        'debug': settings.DEBUG,
        'less_poll': settings.LESS_POLL,
        'angular_base': settings.ANGULAR_BASE,
    }

