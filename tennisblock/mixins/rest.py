import json
from django.http import HttpResponse

class RestMixin(object):

    def render_json(self,context,**response_kwargs):
        """
        An HttpResponse that renders it's content into JSON.
        """
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data,**response_kwargs)


