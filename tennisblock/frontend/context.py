from django.conf import settings

def frontend_context(request):
    return {
        'render_bundles': settings.RENDER_BUNDLES
    }
