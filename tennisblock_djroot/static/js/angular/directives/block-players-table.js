/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockPlayersTable',[ 'BlockPlayers','BlockSubs','BlockSchedule','$q',
    function(BlockPlayers,BlockSubs,BlockSchedule,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'A',
            terminal: false,
            templateUrl: '/static/templates/block-players-table.html',
            //transclude: true,
            replace: false,
            scope: {
                queryDate:    '=queryDate'
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockPlayersTable");

                $scope.players = {
                    guys : [],
                    gals : [],

                    selguys : [],
                    selgals : [],

                    original : {
                        guys : [],
                        gals : []
                    },

                    couples : [],
                    initialized : false,
                    changed : false
                };

                $scope.subs = {
                    'guys' : [],
                    'gals' : [],
                    initialized : false
                };

                $scope.$watch("queryDate",function() {
                    console.log("Querydate has changed!!!!");
                    update();
                });

                var updatePlayers = function(data) {
                    $scope.players.guys = data.guys;
                    $scope.players.gals = data.gals;
                    $scope.players.selguys = data.guys.slice(0);
                    $scope.players.selgals = data.gals.slice(0);
                    $scope.players.original.guys = data.guys.slice(0);
                    $scope.players.original.gals = data.gals.slice(0);

                    $scope.players.couples = _.map($scope.players.guys,function(guy) {
                        var pid = guy.partner;
                        if (pid) {
                            var pgal = _.find($scope.players.gals,function(gal) {
                                return gal.id == pid;
                            });
                            if (pgal) {
                                return {
                                    guy: {
                                        id      : guy.id,
                                        name    : guy.name
                                    },
                                    gal : {
                                        id      : pgal.id,
                                        name    : pgal.name
                                    }
                                };
                            }
                        }
                    });
                    $scope.players.originalcouples = JSON.parse(JSON.stringify($scope.players.couples));
                    //$scope.players.couples = _.zip($scope.players.guys,$scope.players.gals);
                    $scope.players.initialized = true;
                    console.log("Updated Block Players for date:" + $scope.queryDate);
                };

                var updateSubs = function(data) {
                    $scope.subs.guys = data.guysubs;
                    $scope.subs.gals = data.galsubs;
                    $scope.subs.initialized = true;
                };

                var update = function() {

                    var pdef = $q.defer();
                    BlockPlayers.get({'date' : $scope.queryDate},function(data) {
                        pdef.resolve(data);
                    });

                    var sdef = $q.defer();
                    BlockSubs.get({'date' : $scope.queryDate},function(data) { sdef.resolve(data)});

                    $q.all([pdef.promise,sdef.promise]).then(function(results) {
                        console.log("Both are done");
                        updatePlayers(results[0]);
                        updateSubs(results[1]);
                    });
                };

                update();


                $scope.getGuySubs = function(idx,currPlayer) {
                    $scope.players.couples[idx].currguy = currPlayer;
                    return _.union([currPlayer],$scope.subs.guys);
                };
                $scope.getGalSubs = function(idx,currPlayer) {
                    $scope.players.couples[idx].currgal = currPlayer;
                    return _.union([currPlayer],$scope.subs.gals);
                };

                $scope.hasChanged = function() {
                    var cpls= $scope.players.couples;
                    var ocpls= $scope.players.originalcouples;
                    var changed = false;
                    _.each(cpls,function(c,idx) {
                        var oc = ocpls[idx];
                        changed = changed || c.guy.id != oc.guy.id || c.gal.id != oc.gal.id;
                    });
                    console.log("hasChanged: " + changed);
                    return changed;
                };

                $scope.onGuyChanged = function(idx) {
                    var is = $scope.players.couples[idx].guy;
                    var was = $scope.players.couples[idx].currguy;
                    console.log("onGuyChanged[" + idx + "] was " + was.name + " now is " + is.name);
                    $scope.players.couples[idx].currguy = is;
                    var isidx = $scope.subs.guys.indexOf(is);
                    $scope.subs.guys[isidx] = was;
                };


                $scope.onGalChanged = function(idx) {
                    var is = $scope.players.couples[idx].gal;
                    var was = $scope.players.couples[idx].currgal;
                    console.log("onGalChanged[" + idx + "] was " + was.name + " now is " + is.name);
                    $scope.players.couples[idx].currgal = is;
                    var isidx = $scope.subs.gals.indexOf(is);
                    $scope.subs.gals[isidx] = was;
                };

                $scope.updateSchedule = function() {

                    var params = {
                        date:$scope.queryDate
                    };
                    var payload = {
                        couples:$scope.players.couples
                    };

                    BlockPlayers.save(params,payload,function(data){
                        console.log("Schedule updated..");
                        update();
                    },function(data, errr, stuff) {
                        console.log("BlockPlayers update failed:" + errr);
                    });

                };

                /**
                 * schedulePlayersConfirm
                 *
                 * If there is an existing schedule, then confirm that
                 * the user wants to re-schedule before firing the
                 * schedule command.
                 */
                $scope.schedulePlayersConfirm = function() {
                    if ($scope.players.guys.length > 0) {
                        $('#dialog_confirm').dialog({
                            resizable: false,
                            height: 140,
                            modal:true,
                            title:"Reset Schedule",
                            buttons: {
                                "Reset current schedule?": function() {
                                    $(this).dialog("close");
                                    $scope.schedulePlayers();
                                },
                                Cancel: function() {
                                    $(this).dialog("close");
                                }
                            }
                        });
                    } else {
                        $scope.schedulePlayers();
                    }
                };

                /**
                 * schedulePlayers
                 *
                 * Schedule or reschedule the current active date.
                 */
                $scope.schedulePlayers = function() {
                    console.log("Updating the schedule for " + $scope.queryDate);
                    BlockSchedule.save({date:$scope.queryDate},function(data){
                        console.log("Done");
                        update();
                    },function(data, errr, stuff) {
                        console.log("Error" + errr);
                    });
                };

            }
        };
    }
]);

