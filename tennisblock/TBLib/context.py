from __future__ import absolute_import

from os.path import join

from django.conf import settings


def tennisblock(request):

    return {
        'debug' : settings.DEBUG,
        'less_poll': settings.LESS_POLL,
        }

