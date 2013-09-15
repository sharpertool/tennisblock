// Avoid issues in IE* where console is not defined!
if (!window.console) {
    window.console = {};
    window.console.log = function() {};
}

if (typeof GBBasePath === 'undefined') {
    GBBasePath = location.protocol + '//' + location.host + "/js/";

    if (location.host.search('localhost') >= 0 || location.host.search("bondinorthpro") >= 0) {
        console.log("Setting up for localhost.");
        GBBasePath = location.protocol + '//' + location.host + "/static/js/";
    }
}
