/* retrieve all elements of a given class */
function getElementsByClass(search)
{
    var classElements = new Array();
    var els = document.getElementsByTagName('*');
    var pattern = new RegExp('(^|\\s)' + search + '(\\s|$)');

    for (var i = 0, j = 0; i < els.length; i++)
    {
        if (pattern.test(els[i].className))
        {
            classElements[j] = els[i];
            j++;
        }
    }
    
    return classElements;
}

/* create an XML HTTP Request object for "ajax" calls */
function createXMLHTTPObject()
{
    if (typeof XMLHttpRequest != 'undefined')
    {
        return new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        var vers = [
            'Microsoft.XmlHttp',
            'MSXML2.XmlHttp',
            'MSXML2.XmlHttp.3.0',
            'MSXML2.XmlHttp.4.0',
            'MSXML2.XmlHttp.5.0'
        ];

        for (var i = vers.length - 1; i >= 0; i--)
        {
            try
            {
                httpObj = new ActiveXObject(vers[i]);
                return httpObj;
            }
            catch(e) {}
        }
    }
    throw new Error('XMLHTTP not supported');
}

