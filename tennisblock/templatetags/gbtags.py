from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()
import os.path
import re

lessFiles = []
cssFiles = []

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

def isFixedUrl(url):
    return re.search('^http',url,re.I) or re.search('^//',url)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(is_safe=True)
def scriptFilter(s):
    """
    Filter used to generate javascript script tags
    """
    print("Filtering %s" % s)
    if isFixedUrl(s):
        return '<script type="text/javascript" src="%s"></script>' % s
    else:
        return '<script type="text/javascript" src="/static/js/%s"></script>' % s

@register.filter(is_safe=True)
def stylesheetFilter(s,sheettype="css"):
    """
    Filter used on the stylesheets.

    Determines the proper type of stylesheet to use, as well as the stylesheet
    path.
    """
    print("Stylesheet Filtering %s => %s" % (sheettype,s))
    reltype = "stylesheet"
    if sheettype == 'less':
        reltype = "stylesheet/less"
    if isFixedUrl(s):
        return '<link href="%s" rel="%s" media="screen" type="text/css" />' % (s,reltype)
    else:
        if sheettype == 'less':
            sout = ""
            #media = 'only screen and (max-width:480px)'
            media = 'screen'
            sout += '<link href="/static/%s/%s" rel="%s" media="%s" type="text/css" />' % (sheettype,s,reltype,media)
            #media = 'only screen and (min-width:481px)'
            #sout += '<link href="/static/%s/%s" rel="%s" media="%s" type="text/css" />' % (sheettype,s,reltype,media)
            return sout
        else:
            return '<link href="/static/%s/%s" rel="%s" media="screen" type="text/css" />' % (sheettype,s,reltype)

@register.filter(is_safe=True)
def urlfilter(url):
    if not isFixedUrl(url):
        return 'http://'+url
    return url

@register.filter(needs_autoescape=True)
def makeLinkFilter(text,url,autoescape=None):
    if url == "":
        return text

    if not isFixedUrl(url):
        url = 'http://'+url

    return  mark_safe('<a href="%s" target="_blank">%s</a>' % (url,text))


def do_makeLink(parser, token):
    tag_name, text,url = token.split_contents()
    return LinkNode(text,url)
register.tag('makeLink',do_makeLink)

class LinkNode(template.Node):
    def __init__(self, text,link):
        self.text = text
        self.link = link

    def render(self, context):
        return '<a href="%s" target="_blank">%s</a>' % (self.link,self.text)

@register.filter(is_safe=True)
def phonefilter(phone):
    phone = re.sub('\s','',phone) # remove spaces
    m = re.match('(\d{3})(\d{4})',phone)
    if m:
        # No area code
        return "(208) " + m.group(1) + '-' + m.group(2)

    m = re.match('(\d{3})(\d{3})(\d{4})',phone)
    if m:
        return "(%s) %s-%s" % (m.group(1),m.group(2),m.group(3))

    return phone


@register.filter(is_safe=True)
def gbformat(s):
    return 'Filtered:%s' % s

@register.filter(is_safe=True)
def gbless(s):
    return '<link href="%s" media="screen" rel="stylesheet/less" type="text/css" />' % s

@register.filter(is_safe=True)
def gbcss(s):
    return '<link href="%s" media="screen" rel="stylesheet/css" type="text/css"  />' % s

@register.filter(is_safe=True)
def gbjs(s):
    return '<script type="text/javascript" src="%s" ></script>' % s

@register.tag
def gbstylesheet(a,stylesheet):
    """
    Generate a style sheet reference
    """

    (file,ext) = os.path.splitext(stylesheet)
    if ext == '.less':
        lessFiles.append('<link rel="stylesheet/less" type="text/css" href="%s" />' % stylesheet)
    elif ext == '.css':
        cssFiles.append('<link rel="stylesheet/css" type="text/css" href="%s" />' % stylesheet)

    return ""

@register.tag
def gbrenderstyles(a):
    """
    Render the stylesheets for the app
    """
    s = "<!-- Rendering stylesheets from GB Tags -->\n"

    s = s + "\n".join(cssFiles)
    s = s + "\n".join(lessFiles)

    return s



