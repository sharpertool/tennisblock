/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockPlayers',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'A',
            terminal: false,
            templateUrl: '/static/templates/block-players.html',
            transclude: true,
            replace: true,
            scope: {
                couples: '=',
                guys:   '=guys',
                gals:   '=gals'
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockPlayers");
            }
        };
    }
]);

