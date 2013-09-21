// Avoid issues in IE* where console is not defined!
if (!window.console) {
    window.console = {};
    window.console.log = function() {};
}

if (typeof TennisBasePath === 'undefined') {
    TennisBasePath = location.protocol + '//' + location.host + "/static/js/";

    if (location.host.search('localhost') >= 0 || location.host.search("bondinorthpro") >= 0) {
        console.log("Setting up for localhost.");
        TennisBasePath = location.protocol + '//' + location.host + "/static/js/";
    }
}
