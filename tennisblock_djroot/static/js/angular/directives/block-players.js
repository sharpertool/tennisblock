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
            templateUrl: '/static/js/angular/templates/block-players.html',
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

tennisblockapp.directive('blockPlayersTable',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'A',
            terminal: false,
            templateUrl: '/static/js/angular/templates/block-players-table.html',
            //transclude: true,
            replace: false,
            scope: {
                players:    '=players',
                subs:       '=subs'
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockPlayersTable");

                $scope.getGuySubs = function(currPlayer) {
                    return _.union([currPlayer],$scope.subs.guys);
                };
                $scope.getGalSubs = function(currPlayer) {
                    return _.union([currPlayer],$scope.subs.gals);
                };

                $scope.onPlayerChanged = function(idx,galnguy) {
                    if (galnguy) {
                        var players = $scope.players.gals;
                        var subs = $scope.subs.gals;
                        var selplayers = $scope.players.selgals;
                    } else {
                        var players = $scope.players.guys;
                        var subs = $scope.subs.guys;
                        var selplayers = $scope.players.selguys;
                    }
                    var was = players[idx];
                    var is = selplayers[idx];
                    console.log("onPlayerChanged[" + idx + "][" + galnguy + "] was " + was.name + " now is " + is.name);
                    $scope.players.changed = true;

                    var isidx = subs.indexOf(is);
                    console.log("isindex:" + isidx);
                    subs[isidx] = was;
                    players[idx] = is;
                };
            }
        };
    }
]);

/*
partsimApplication.directive( "sidebarSection",
    [ "categories",
        function( categories ){
            return {
                "require": "^sidebarAccordion",
                "controller": "SidebarController",
                "restrict": "E",
                "transclude": true,
                "replace": true,
                "templateUrl": "js/eeweb/angular/template/sidebar-section.tpl.html",
                "scope": {
                    "heading": "@",
                    "section": "@"
                },
                "link": function( scope, element, attributes, controller ){

                    controller.addGroup( scope );

                    scope.isOpen = false;
                    scope.categories = [ ];

                    if( scope.section == "diagramming" ){
                        //TODO: Do something about diagramming here.
                        //TODO: How do we translate the title here?
                        scope.categories = [ {
                            "name": "Basic Shapes",
                            "title": "Basic Shapes",
                            "subcategory": "Basic_Shapes-Sub"
                        } ];
                    }else{
                        if( "promise" in scope ){
                            return;
                        }
                        scope.promise = categories.load( scope.section )
                            .then( function( categories ){
                                if( !_.isEmpty( categories ) ){
                                    scope.categories = categories;
                                }else{
                                    delete scope.promise;
                                }
                            }, function( error ){
                                delete scope.promise;
                                //TODO: Do something with error here.
                            } );
                    }

                    scope.$watch( "isOpen",
                        function( value ){
                            if( value ){
                                controller.closeOthers( scope );
                            }
                        } );

                    scope.onEnter = function() {

                    };
                }
            };
        } ] );
*/
