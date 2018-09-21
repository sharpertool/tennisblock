/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/20/13
 * Time: 2:44 PM
 */

tennisblockapp.directive('scheduleNav',['Members','$q',
    function(Members,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            //require: '^blockMembers',
            controller: 'BlockSchedule',
            terminal: false,
            templateUrl: '/static/templates/schedule-nav.html',
            transclude: true,
            replace: true,
            scope: {
                block : '='
            },
            link: function($scope,$element,$attributes,ctrl) {
            }
        }
    }
]);

