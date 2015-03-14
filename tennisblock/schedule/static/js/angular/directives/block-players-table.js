/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockPlayersTable',[
        'BlockPlayers','BlockSubs','BlockSchedule','SendSchedule','$q','$location',
    function(BlockPlayers,BlockSubs,BlockSchedule,SendSchedule,$q,$location) {
        // Initialization

        return {
            priority: 10,
            restrict: 'A',
            terminal: false,
            controller: 'BlockSchedule',
            templateUrl: '/static/templates/block-players-table.html',
            //transclude: true,
            replace: false,
            scope: {
                queryDate:    '=queryDate'
            },
            link: function($scope,$element,$attributes,ctrl) {
                console.log("Link blockPlayersTable");

                var ver = 1;

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
                        return {
                            guy: {
                                id: guy.id,
                                name: guy.name
                            },
                            gal: {
                                name: '----'

                            }
                        };
                    });
                    $scope.players.originalcouples = JSON.parse(JSON.stringify($scope.players.couples));
                    //$scope.players.couples = _.zip($scope.players.guys,$scope.players.gals);
                    $scope.players.initialized = true;
                    console.log("Updated Block Players for date:" + $scope.queryDate);
                };

                var updateSubs = function(data) {
                    $scope.subs.guys = data.guysubs;
                    $scope.subs.gals = data.galsubs;

                    $scope.subs.guys.push({'name': '----'});
                    $scope.subs.gals.push({'name': '----'});
                    $scope.subs.initialized = true;
                };

                var update = function() {

                    ver += 1;
                    var pdef = $q.defer();
                    BlockPlayers.get({'date' : $scope.queryDate, 'ver' : ver},function(data) {
                        pdef.resolve(data);
                    });

                    var sdef = $q.defer();
                    BlockSubs.get({'date' : $scope.queryDate, 'ver' : ver},function(data) {
                        sdef.resolve(data)
                    });

                    $q.all([pdef.promise,sdef.promise]).then(function(results) {
                        console.log("Both are done");
                        updatePlayers(results[0]);
                        updateSubs(results[1]);
                    });
                };

                update();


                /**
                 * p.name for p in getGuySubs($index,couple.guy)
                 * @param idx
                 * @param currPlayer
                 * @returns {*}
                 */
                $scope.getGuySubs = function(idx,currPlayer) {
                    if (currPlayer && $scope.players.couples[idx]) {

                        $scope.players.couples[idx].currguy = currPlayer;
                        return _.union([currPlayer],$scope.subs.guys);
                    }
                    return $scope.subs.guys;
                };

                $scope.getGalSubs = function(idx,currPlayer) {
                    if (currPlayer && $scope.players.couples[idx]) {

                        $scope.players.couples[idx].currgal = currPlayer;
                        return _.union([currPlayer],$scope.subs.gals);
                    }
                    return $scope.subs.gals;
                };

                $scope.hasChanged = function() {
                    var cpls= $scope.players.couples;
                    var ocpls= $scope.players.originalcouples;
                    var changed = false;
                    _.each(cpls,function(c,idx) {
                        if (typeof c == 'undefined') {
                            console.log("Null entry in one of the players..");
                        } else {
                            var oc = ocpls[idx];
                            changed = changed || c.guy.id != oc.guy.id || c.gal.id != oc.gal.id;
                        }
                    });
                    console.log("hasChanged: " + changed);
                    return changed;
                };

                /**
                 * Update the player and sub list when a new player is selected.
                 *
                 * idx is the couple index, and ptype is 'gal' or 'guy'
                 *
                 * When the selection changes, the couple[ptype] is updated.
                 * Keep track of the current guy in couple['curr+ptype] so we can tell
                 * who was previously selected, and put them back in as a possible sub.
                 *
                 * We remove the new 'is' ptype, and add the previous ptype in the same index.
                 * @param idx
                 */
                $scope.onPlayerChanged = function onPlayerChanged(idx, ptype) {
                    var couple = $scope.players.couples[idx];
                    var subs = $scope.subs[ptype+'s'];

                    var is = couple[ptype]; // Controlled by selector
                    var was = couple['curr'+ptype]; // So I can track previous value on change
                    console.log("onPlayerChanged[" + idx + "] was " + was.name + " now is " + is.name);
                    couple['curr'+ptype] = is;

                    if (is.name === '----') {
                        // Don't remove this one, just add the new player to the sub list.
                        subs.splice(-1,0,was);
                    } else {
                        var isidx = subs.indexOf(is);
                        if (was.name === '----') {
                            // Remove the is from the list
                            subs.splice(isidx,1);
                        } else {
                            var isidx = subs.indexOf(is);
                            if (isidx >=0 ){
                                subs[isidx] = was;
                            }
                        }
                    }
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
                        ctrl.updateAll();
                        amplify.publish(tb.events.SCHED_UPDATED);
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
                 * schedulePlayersConfirm
                 *
                 * If there is an existing schedule, then confirm that
                 * the user wants to re-schedule before firing the
                 * schedule command.
                 */
                $scope.clearScheduleConfirm = function() {
                    if ($scope.players.guys.length > 0) {
                        $('#dialog_confirm').dialog({
                            resizable: false,
                            height: 140,
                            modal:true,
                            title:"Reset Schedule",
                            buttons: {
                                "Clear current schedule?": function() {
                                    $(this).dialog("close");
                                    $scope.clearSchedule();
                                },
                                Cancel: function() {
                                    $(this).dialog("close");
                                }
                            }
                        });
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

                /**
                 * schedulePlayers
                 *
                 * Schedule or reschedule the current active date.
                 */
                $scope.clearSchedule = function() {
                    console.log("Clearing the schedule for " + $scope.queryDate);
                    BlockSchedule.remove({date:$scope.queryDate},function(){
                        console.log("Done");
                        update();
                    },function(data, errr, stuff) {
                        console.log("Error" + errr);
                    });
                };

                /**
                 * sendScheduleUpdate
                 *
                 * Send out an e-mail with the schedule for this date.
                 */
                $scope.sendScheduleUpdate = function() {
                    window.location = window.location.origin
                        + "/schedule/notify/" + $scope.queryDate +"/";
                    //SendSchedule.update({date:$scope.queryDate},function() {});
                }
            }
        };
    }
]);

