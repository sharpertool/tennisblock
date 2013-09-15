# Create your views here.


from django.views.generic import TemplateView

from blockdb.models import *

class MembersView(TemplateView):
    d = {
        #'images'        : images,
        'angularapp'    : 'gardenbuzz',
        #'isprod'        : settings.PROD
    }

    template_name = "members.html"
