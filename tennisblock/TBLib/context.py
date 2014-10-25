from __future__ import absolute_import

from django.conf import settings


def tennisblock(request):
    return {
        'angularapp': 'tennisblock',
        'debug': settings.DEBUG,
        'angular_base': settings.ANGULAR_BASE,
        'USE_LESS': settings.USE_LESS,
        'LESS_POLL': settings.LESS_POLL
    }

