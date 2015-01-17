/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('membersList',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/js/angular/templates/members-list.html',
            transclude: true,
            replace: true,
            scope: false,
            link: function($scope,$element,$attributes) {
                console.log("Link membersList");
            }
        };
    }
]);

