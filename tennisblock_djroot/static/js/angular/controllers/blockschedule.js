/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */

app.factory('ScheduleResource', function($resource){
        return $resource('/api/blockschedule/:date/', {}, {
            query: {method:'GET', params:{date:'2013-09-20'}, isArray:false},
            post: {method:'post',isArray:false},
            put: {method:'post',isArray:false}
        })
}).factory('BlockDates',function($resource){
        return $resource('/api/blockdates/', {}, {
            query: {method:'GET', isArray:true}
        })
}).factory('BlockPlayers',function($resource){
        return $resource('/api/blockplayers/:date/', {}, {
            query: {method:'GET', params:{date:'2013-09-20'}, isArray:false}
        })
}).factory('BlockSubs',function($resource){
        return $resource('/api/subs/:date/', {}, {
            query: {method:'GET', params:{date:'2013-09-20'}, isArray:false}
        })
});

app.controller('BlockSchedule', function blocksched($scope,$http,ScheduleResource,BlockDates,BlockPlayers,BlockSubs) {
    $scope.dates = [];
    $scope.guys = [];
    $scope.gals = [];
    $scope.subs = {
        'guys' : [],
        'gals' : []
    }
    $scope.queryDate = null;
    $scope.initialized = false;

    var updateInitialized = function updateinit() {
        if ($scope.dates.length > 0
            && $scope.guys.length > 0
            && $scope.gals.length > 0) {
            $scope.initialized = true;
        } else {
            $scope.initialized = false;
        }

        $scope.isLastDate = isLastBlockDate();
        $scope.isFirstDate = isFirstBlockDate();
    };

    BlockDates.query(function bdates(data) {
        $scope.dates= data;
        $scope.firstDate = tb.utils.pyDate2js(data[0].date);
        $scope.lastDate = tb.utils.pyDate2js(data[data.length-1].date);
        $scope.blocksched = {};
        _.each(data,function(d) {
            var bdate = tb.utils.pyDate2js(d.date);
            var ho = d.holdout;
            $scope.blocksched[bdate] = ho;
        });
        updateInitialized();
    });

    var updateAll = function updateAll() {
        $scope.initialized = false;

        BlockPlayers.query({'date' : $scope.queryDate},function bplayers(data) {
                $scope.currdate = tb.utils.pyDate2js(data.date).toLocaleDateString();
                $scope.guys = data.guys;
                $scope.gals = data.gals;
                updateInitialized();
            });

        BlockSubs.query({'date' : $scope.queryDate},function bsubs(data) {
                $scope.subs.guys = data.guysubs;
                $scope.subs.gals = data.galsubs;
                updateInitialized();
            });

        ScheduleResource.query({'date' : $scope.queryDate},
            function schedule(data) {
                $scope.slots= data;
                updateInitialized();
            });
    };

    var isLastBlockDate = function islbd() {
        if ($scope.lastDate && $scope.currdate) {
            return $scope.currdate == $scope.lastDate.toLocaleDateString();
        }

        return false;
    };

    var isFirstBlockDate = function isfbd() {
        if ($scope.firstDate && $scope.currdate) {
            return $scope.currdate == $scope.firstDate.toLocaleDateString();
        }
        return false;
    };

    var previousBlockDate = function pbd() {
        var d1 = new Date($scope.currdate);
        if (d1.toDateString() == $scope.firstDate.toDateString()) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()-7);
        while (d2.toDateString() != $scope.lastDate.toDateString() && $scope.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d2.getDate()-7);
        }

        return d2;
    };

    var nextBlockDate = function nbd() {
        var d1 = new Date($scope.currdate);
        if (d1.toDateString() == $scope.lastDate.toDateString()) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()+7);
        while (d2.toDateString() != $scope.lastDate.toDateString() && $scope.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d2.getDate()+7);
        }

        return d2;
    };

    /**
     * schedulePlayer
     *
     * Update the schedule for the current block session
     */
    $scope.schedulePlayers = function() {
        console.log("Updating the schedule for " + $scope.queryDate);
        ScheduleResource.post({date:$scope.queryDate},function(data){
            console.log("Done");
        },function(data, errr, stuff) {
            console.log("Error" + errr);
        });
    };

    $scope.pickTeams = function() {
        console.log("Picking Teams ");
        ScheduleResource.put({date:$scope.queryDate},function(data){
            console.log("Done Picking Teams");
        },function(data, errr, stuff) {
            console.log("Error Picking Teams:" + errr);
        });
    };

    $scope.playSheet = function() {
        $http({method:"GET",url:'/api/blocksheet/'}).success(function(sheet) {
            console.log("Returned something..");
        }).error(function(a,b,c) {
            console.log('returned nothing');
        });
    };

    $scope.isHoldout = function isho() {

    };

    $scope.gotodate = function gotod(date) {
        $scope.queryDate = date;
        updateAll();
    };

    $scope.previous = function() {
        var d1 = previousBlockDate();
        $scope.queryDate = tb.utils.jsDate2py(d1);
        updateAll();
    };

    $scope.next = function() {
        $scope.queryDate = tb.utils.jsDate2py(nextBlockDate());
        updateAll();
    };

    updateAll();
});


