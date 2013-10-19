/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockMember',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/js/angular/templates/block-member.html',
            //transclude: true,
            replace: false,
            scope: false,
            link: function($scope,$element,$attributes) {
                console.log("Link blockMember");
            }
        };
    }
]);

