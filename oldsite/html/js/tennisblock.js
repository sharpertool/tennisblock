/**
 *
 */
var myBlock =
{
    /**
     * Class: mxClient
     *
     * Bootstrapping mechanism for the mxGraph thin client. The production version
     * of this file contains all code required to run the mxGraph thin client, as
     * well as global constants to identify the browser and operating system in
     * use. You may have to load chrome://global/content/contentAreaUtils.js in
     * your page to disable certain security restrictions in Mozilla.
     *
     * Variable: VERSION
     *
     * Contains the current version of the mxGraph library. The strings that
     * communicate versions of mxGraph use the following format.
     *
     * versionMajor.versionMinor.buildNumber.revisionNumber
     *
     * Current version is 1.8.0.6.
     */
    VERSION:'1.8.0.6',

    /**
    * Variable: IS_IE
    *
    * True if the current browser is Internet Explorer.
    */
    IS_IE:navigator.userAgent.indexOf('MSIE') >= 0,

    /**
    * Variable: IS_IE6
    *
    * True if the current browser is Internet Explorer 6.x.
    */
    IS_IE6:navigator.userAgent.indexOf('MSIE 6') >= 0,

    /**
    * Variable: IS_NS
    *
    * True if the current browser is Netscape (including Firefox).
    */
    IS_NS:navigator.userAgent.indexOf('Mozilla/') >= 0 &&
      navigator.userAgent.indexOf('MSIE') < 0,

    /**
    * Variable: IS_OP
    *
    * True if the current browser is Opera.
    */
    IS_OP:navigator.userAgent.indexOf('Opera/') >= 0,

    /**
    * Variable: IS_OT
    *
    * True if -o-transform is available as a CSS style. This is the case
    * for Opera browsers that use Presto/2.5 and later.
    */
    IS_OT:navigator.userAgent.indexOf('Presto/2.4') < 0 &&
      navigator.userAgent.indexOf('Presto/2.3') < 0 &&
      navigator.userAgent.indexOf('Presto/2.2') < 0 &&
      navigator.userAgent.indexOf('Presto/2.1') < 0 &&
      navigator.userAgent.indexOf('Presto/2.0') < 0 &&
      navigator.userAgent.indexOf('Presto/1') < 0,

    /**
    * Variable: IS_SF
    *
    * True if the current browser is Safari.
    */
    IS_SF:navigator.userAgent.indexOf('AppleWebKit/') >= 0 &&
      navigator.userAgent.indexOf('Chrome/') < 0,

    /**
    * Variable: IS_GC
    *
    * True if the current browser is Google Chrome.
    */
    IS_GC:navigator.userAgent.indexOf('Chrome/') >= 0,

    /**
    * Variable: IS_MT
    *
    * True if -moz-transform is available as a CSS style. This is the case
    * for all Firefox-based browsers newer than or equal 3, such as Camino,
    * Iceweasel, Seamonkey and Iceape.
    */
    IS_MT:(navigator.userAgent.indexOf('Firefox/') >= 0 &&
      navigator.userAgent.indexOf('Firefox/1') < 0 &&
      navigator.userAgent.indexOf('Firefox/2') < 0) ||
      (navigator.userAgent.indexOf('Iceweasel/') >= 0 &&
          navigator.userAgent.indexOf('Iceweasel/1') < 0 &&
          navigator.userAgent.indexOf('Iceweasel/2') < 0) ||
      (navigator.userAgent.indexOf('SeaMonkey/') >= 0 &&
          navigator.userAgent.indexOf('SeaMonkey/1') < 0) ||
      (navigator.userAgent.indexOf('Iceape/') >= 0 &&
          navigator.userAgent.indexOf('Iceape/1') < 0),

    /**
    * Variable: IS_SVG
    *
    * True if the browser supports SVG.
    */
    IS_SVG:navigator.userAgent.indexOf('Firefox/') >= 0 || // FF and Camino
       navigator.userAgent.indexOf('Iceweasel/') >= 0 || // Firefox on Debian
       navigator.userAgent.indexOf('Seamonkey/') >= 0 || // Firefox-based
       navigator.userAgent.indexOf('Iceape/') >= 0 || // Seamonkey on Debian
       navigator.userAgent.indexOf('Galeon/') >= 0 || // Gnome Browser (old)
       navigator.userAgent.indexOf('Epiphany/') >= 0 || // Gnome Browser (new)
       navigator.userAgent.indexOf('AppleWebKit/') >= 0 || // Safari/Google Chrome
       navigator.userAgent.indexOf('Gecko/') >= 0 || // Netscape/Gecko
       navigator.userAgent.indexOf('Opera/') >= 0,

    /**
    * Variable: NO_FO
    *
    * True if foreignObject support is not available. This is the case for
    * Opera and older SVG-based browsers. IE does not require this type
    * of tag.
    */
    NO_FO:navigator.userAgent.indexOf('Firefox/1') >= 0 ||
      navigator.userAgent.indexOf('Iceweasel/1') >= 0 ||
      navigator.userAgent.indexOf('Firefox/2') >= 0 ||
      navigator.userAgent.indexOf('Iceweasel/2') >= 0 ||
      navigator.userAgent.indexOf('SeaMonkey/1') >= 0 ||
      navigator.userAgent.indexOf('Iceape/1') >= 0 ||
      navigator.userAgent.indexOf('Camino/1') >= 0 ||
      navigator.userAgent.indexOf('Epiphany/2') >= 0 ||
      navigator.userAgent.indexOf('Opera/') >= 0 ||
      navigator.userAgent.indexOf('MSIE') >= 0 ||
      navigator.userAgent.indexOf('Mozilla/2') >= 0, // Safari/Google Chrome

    /**
    * Variable: IS_VML
    *
    * True if the browser supports VML.
    */
    IS_VML:navigator.appName.toUpperCase() == 'MICROSOFT INTERNET EXPLORER',

    /**
    * Variable: IS_MAC
    *
    * True if the client is a Mac.
    */
    IS_MAC:navigator.userAgent.toUpperCase().indexOf('MACINTOSH') > 0,

    /**
    * Variable: IS_TOUCH
    *
    * True if this client uses a touch interface (no mouse). Currently this
    * detects IPads, IPods, IPhones and Android devices.
    */
    IS_TOUCH:navigator.userAgent.toUpperCase().indexOf('IPAD') > 0 ||
         navigator.userAgent.toUpperCase().indexOf('IPOD') > 0 ||
         navigator.userAgent.toUpperCase().indexOf('IPHONE') > 0 ||
         navigator.userAgent.toUpperCase().indexOf('ANDROID') > 0,

    /**
    * Variable: IS_LOCAL
    *
    * True if the documents location does not start with http:// or https://.
    */
    IS_LOCAL:document.location.href.indexOf('http://') < 0 &&
     document.location.href.indexOf('https://') < 0,

    /**
    * Function: isBrowserSupported
    *
    * Returns true if the current browser is supported, that is, if
    * <mxClient.IS_VML> or <mxClient.IS_SVG> is true.
    *
    * Example:
    *
    * (code)
    * if (!mxClient.isBrowserSupported())
    * {
    *   mxUtils.error('Browser is not supported!', 200, false);
    * }
    * (end)
    */
    isBrowserSupported:function () {
        return mxClient.IS_VML || mxClient.IS_SVG;
    },

    /**
    * Function: link
    *
    * Adds a link node to the head of the document. Use this
    * to add a stylesheet to the page as follows:
    *
    * (code)
    * mxClient.link('stylesheet', filename);
    * (end)
    *
    * where filename is the (relative) URL of the stylesheet. The charset
    * is hardcoded to ISO-8859-1 and the type is text/css.
    *
    * Parameters:
    *
    * rel - String that represents the rel attribute of the link node.
    * href - String that represents the href attribute of the link node.
    * doc - Optional parent document of the link node.
    */
    link:function (rel, href, doc) {
        doc = doc || document;

        // Workaround for Operation Aborted in IE6 if base tag is used in head
        if (mxClient.IS_IE6) {
            doc.write('<link rel="' + rel + '" href="' + href + '" charset="ISO-8859-1" type="text/css"/>');
        }
        else {
            var link = doc.createElement('link');

            link.setAttribute('rel', rel);
            link.setAttribute('href', href);
            link.setAttribute('charset', 'ISO-8859-1');
            link.setAttribute('type', 'text/css');

            var head = doc.getElementsByTagName('head')[0];
            head.appendChild(link);
        }
    },

    /**
     * Function: include
     *
     * Dynamically adds a script node to the document header.
     *
     * In production environments, the includes are resolved in the mxClient.js
     * file to reduce the number of requests required for client startup. This
     * function should only be used in development environments, but not in
     * production systems.
     */
    include:function (src) {
        document.write('<script src="' + src + '"></script>');
    },

    /**
     * Function: dispose
     *
     * Frees up memory in IE by resolving cyclic dependencies between the DOM
     * and the JavaScript objects. This is always invoked in IE when the page
     * unloads.
     */
    dispose:function () {
        // Cleans all objects where listeners have been added
        for (var i = 0; i < mxEvent.objects.length; i++) {
            if (mxEvent.objects[i].mxListenerList != null) {
                mxEvent.removeAllListeners(mxEvent.objects[i]);
            }
        }
    }

};

