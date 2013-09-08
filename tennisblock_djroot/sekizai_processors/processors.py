
import re

def isFixedUrl(url):
    """
    Detect if the given url is absolute/fixed or relative.
    """
    return re.search('^http',url,re.I) or re.search('^//',url)

def spaceless_post_processor(context, data, namespace):
    from django.utils.html import strip_spaces_between_tags
    return strip_spaces_between_tags(data)

def jsprocessor(context,data,namespace):
    items = re.split("\n",data)
    sout = "    <!-- Rendering Javascript Sekizai incldues for block %s -->\n" % namespace
    for i in items:
        if i:
            if isFixedUrl(i):
                sout = sout +  '    <script type="text/javascript" src="%s"></script>\n' % i.strip()
            else:
                sout = sout +  '    <script type="text/javascript" src="/static%s"></script>\n' % i.strip()
    #print("Rendering Javascript as " + sout)
    return sout

def styleprocessor(context,data,namespace):
    items = re.split("\n",data)
    sout = "    <!-- Rendering stylesheet includes for %s -->\n" % namespace
    if namespace == 'less':
        template = '    <link href="%s" rel="stylesheet/less" media="screen" type="text/css" />\n'
    else:
        template = '    <link href="%s" rel="stylesheet" media="screen" type="text/css" />\n'

    for i in items:
        if i:
            if isFixedUrl(i):
                link = i.strip()
            else:
                link = '/static' + i.strip()

            sout +=  template % link

    return sout

