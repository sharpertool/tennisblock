/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/15/13
 * Time: 8:01 PM
 */


app.directive('fglist', function() {
    var linkFn;
    linkFn = function($scope,element,attrs) {

    };

    return {
        restrict: 'E',
        templateUrl: AngularPartialsBase + '/fglist.html',
        replace: true,
        link: linkFn
    }

});