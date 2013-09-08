/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/15/13
 * Time: 8:01 PM
 */


app.directive('fgquestions', function() {
    var linkFn;
    linkFn = function($scope,element,attrs) {

    };

    return {
        restrict: 'E',
        templateUrl: AngularPartialsBase + '/fgquestions.html',
        replace: true,
        link: linkFn
    }

});
