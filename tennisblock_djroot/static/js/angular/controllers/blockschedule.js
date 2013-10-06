/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */

tennisblockapp.controller('BlockSchedule', function blocksched($scope,$http,
                                                    BlockDates,
                                                    BlockPlayers,BlockSubs,PickTeams,
                                                    PlaySheet,TeamSchedule,BlockSchedule
    ) {
    $scope.block = {
        dates : [],
        currdate : null,
        firstDate : null,
        lastDate : null,
        blocksched : {},
        isFirstDate : false,
        isLastDate : false,
        queryDate : null,
        initialized : false
    };
    $scope.players = {
        guys : [],
        gals : [],

        selguys : [],
        selgals : [],

        couples : [],
        initialized : false
    };
    $scope.subs = {
        'guys' : [],
        'gals' : [],
        initialized : false
    };
    $scope.match = {
        'sets' : []
    };

    $scope.view = {
        initialized : false
    };

    var updateInitialized = function updateinit() {
        if ($scope.block.initialized
            && $scope.players.initialized
            && $scope.subs.initialized) {
            $scope.view.initialized = true;
        } else {
            $scope.view.initialized = false;
        }

        $scope.block.isLastDate = isLastBlockDate();
        $scope.block.isFirstDate = isFirstBlockDate();
    };

    BlockDates.query(function bdates(data) {
        $scope.block.dates= data;
        $scope.block.firstDate = tb.utils.pyDate2js(data[0].date);
        $scope.block.lastDate = tb.utils.pyDate2js(data[data.length-1].date);
        $scope.block.blocksched = {};
        _.each(data,function(d) {
            var bdate = tb.utils.pyDate2js(d.date);
            var ho = d.holdout;
            if (d.current) {
                $scope.block.currdate = tb.utils.pyDate2js(d.date).toLocaleDateString();
                $scope.block.activedate = $scope.block.currdate;
                $scope.block.queryDate = tb.utils.jsDate2py($scope.block.currdate);
            }

            $scope.block.blocksched[bdate] = ho;
        });
        updateInitialized();
    });

    var resetScope = function() {
        $scope.view.initialized = false;
        $scope.subs.initialized = false;
        $scope.players.initialzed = false;
        $scope.block.initialized = false;
        $scope.players.guys = [];
        $scope.players.gals = [];
        $scope.subs.guys = [];
        $scope.subs.gals = [];
    };

    var updateAll = function updateAll() {
        resetScope();

        BlockPlayers.get({'date' : $scope.block.queryDate},function bplayers(data) {
            $scope.players.guys = data.guys;
            $scope.players.gals = data.gals;
            $scope.players.selguys = data.guys.slice(0);
            $scope.players.selgals = data.gals.slice(0);
            $scope.players.couples = _.zip($scope.players.guys,$scope.players.gals);
            $scope.players.initialized = true;
            console.log("Updated Block Players for date:" + $scope.block.queryDate);
            updateInitialized();
        });

        BlockSubs.get({'date' : $scope.block.queryDate},function bsubs(data) {
            $scope.subs.guys = data.guysubs;
            $scope.subs.gals = data.galsubs;
            $scope.subs.initialized = true;
            updateInitialized();
        });

        TeamSchedule.get({'date' : $scope.block.queryDate}, function(data) {
            $scope.match.sets = data.match;
        });
    };

    var isLastBlockDate = function islbd() {
        if ($scope.block.lastDate && $scope.block.currdate) {
            return $scope.block.currdate == $scope.block.lastDate.toLocaleDateString();
        }

        return false;
    };

    var isFirstBlockDate = function isfbd() {
        if ($scope.block.firstDate && $scope.block.currdate) {
            return $scope.block.currdate == $scope.block.firstDate.toLocaleDateString();
        }
        return false;
    };

    var previousBlockDate = function pbd() {
        var d1 = new Date($scope.block.currdate);
        if (d1.toDateString() == $scope.block.firstDate.toDateString()) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()-7);
        while (d2.toDateString() != $scope.block.lastDate.toDateString() && $scope.block.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d2.getDate()-7);
        }

        return d2;
    };

    var nextBlockDate = function nbd() {
        var d1 = new Date($scope.block.currdate);
        if (d1.toDateString() == $scope.block.lastDate.toDateString()) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()+7);
        while (d2.toDateString() != $scope.block.lastDate.toDateString() && $scope.block.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d2.getDate()+7);
        }

        return d2;
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
        console.log("Updating the schedule for " + $scope.block.queryDate);
        BlockSchedule.save({date:$scope.block.queryDate},function(data){
            console.log("Done");
            updateAll();
        },function(data, errr, stuff) {
            console.log("Error" + errr);
        });
    };

    $scope.pickTeams = function() {
        console.log("Picking Teams for " + $scope.block.queryDate);
        PickTeams.save({date: $scope.block.queryDate},function(data){
            console.log("Done Picking Teams:" + data.status + " " + data.date);
            updateAll();
        },function(data, e, stuff) {
            console.log("Error Picking Teams:" + e);
        });
    };

    $scope.playSheet = function() {
        PlaySheet.get({data:$scope.block.queryDate});
    };

    $scope.isHoldout = function isho() {

    };

    $scope.gotodate = function gotod(date) {
        console.log("Setting new queryDate to " + date);
        $scope.block.queryDate = date;
        console.log("queryDate set to " + $scope.block.queryDate);
        updateAll();
    };

    $scope.previous = function() {
        var d1 = previousBlockDate();
        $scope.block.queryDate = tb.utils.jsDate2py(d1);
        console.log("queryDate set to " + $scope.block.queryDate);
        updateAll();
    };

    $scope.next = function() {
        $scope.block.queryDate = tb.utils.jsDate2py(nextBlockDate());
        console.log("queryDate set to " + $scope.block.queryDate);
        updateAll();
    };

    $scope.playerPairs = function() {
        return couples;
    };

    $scope.filterPlayerSub = function(player,subs) {
        a = subs.clone();
        a.push(player);
    };

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

        var isidx = subs.indexOf(is);
        console.log("isindex:" + isidx);
        subs[isidx] = was;
        players[idx] = is;
    };

    updateAll();
});


