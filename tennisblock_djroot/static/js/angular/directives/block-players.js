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

tennisblockapp.directive('blockPlayersTable',[ 'BlockPlayers',
    function(BlockPlayers) {
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
                subs:       '=subs',
                block:      '=block'
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockPlayersTable");

                $scope.original = {
                    guys : [],
                    gals : []
                };

                $scope.$watch('players',function() {
                    $scope.original.guys = $scope.players.guys.slice(0);
                    $scope.original.gals = $scope.players.gals.slice(0);
                    console.log("Updated the original snapshot.");
                });

                $scope.getGuySubs = function(currPlayer) {
                    return _.union([currPlayer],$scope.subs.guys);
                };
                $scope.getGalSubs = function(currPlayer) {
                    return _.union([currPlayer],$scope.subs.gals);
                };

                $scope.hasChanged = function() {
                    var changed = (_.difference($scope.players.guys,$scope.players.original.guys).length
                    + _.difference($scope.players.gals,$scope.players.original.gals).length) > 0;
                    console.log("hasChanged: " + changed);
                    return changed;
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

                $scope.updateSchedule = function() {

                    var params = {
                        date:$scope.block.queryDate
                    };
                    var payload = {
                        guys:$scope.players.guys,
                        gals:$scope.players.gals
                    };

                    BlockPlayers.save(params,payload,function(data){
                        console.log("Schedule updated..");
                    },function(data, errr, stuff) {
                        console.log("BlockPlayers update failed:" + errr);
                    });

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
