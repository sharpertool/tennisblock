from django.conf import settings

def frontend_context(request):
    return {
        "render_bundles": settings.RENDER_BUNDLES,
        "sentry_dsn": settings.DJANGO_SENTRY_DSN,
    }
