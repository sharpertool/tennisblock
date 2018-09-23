from django.conf import settings


def tennisblock(request):
    return {
        'angularapp': 'tennisblock',
        'debug': settings.DEBUG,
    }
