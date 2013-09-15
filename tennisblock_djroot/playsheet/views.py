# Create your views here.


from django.views.generic import TemplateView

from blockdb.models import *

class PlaysheetView(TemplateView):
    d = {
        #'images'        : images,
        'angularapp'    : 'gardenbuzz',
        #'isprod'        : settings.PROD
    }

    template_name = "playsheet.html"
