from __future__ import absolute_import

from django.conf import settings


def tennisblock(request):
    return {
        'angularapp': 'tennisblock',
        'debug': settings.DEBUG,
        'use_local_bundle': settings.USE_LOCAL_BUNDLE
    }

