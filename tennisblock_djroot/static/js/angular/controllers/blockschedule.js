/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */


app.controller('BlockSchedule', function($scope,$http) {
    $scope.dates = [];
    $scope.guys = [];
    $scope.gals = [];
    $scope.subs = [];
    $scope.queryDate = null;
    $scope.initialized = false;

    var updateInitialized = function() {
        if ($scope.dates.length > 0
            && $scope.guys.length > 0
            && $scope.gals.lengty > 0) {
            $scope.initialized = true;
        } else {
            $scope.initialized = false;
        }
    };

    $http.get('/api/blockdates').success(function(data) {
        $scope.dates= data;
        $scope.firstDate = data[0].date;
        $scope.lastDate = data[data.length-1].date;
        $scope.blocksched = {};
        _.each(data,function(d) {
            var bdate = d.date;
            var ho = d.holdout;
            $scope.blocksched[bdate] = ho;
        });
        updateInitialized();
    });

    var updateAll = function() {
        $scope.initialized = false;

        $http({
            'url'       :'/api/blockplayers/',
            'method'    : 'GET',
            'params'    : {'date' : $scope.queryDate}
        }).success(function(data) {
                $scope.currdate = data.date;
                $scope.guys = data.guys;
                $scope.gals = data.gals;
                updateInitialized();
            });

        $http({
            'url'       :'/api/subs/',
            'method'    : 'GET',
            'params'    : {'date' : $scope.queryDate}
        }).success(function(data) {
                $scope.subs = data;
                updateInitialized();
            });

        $http({
            'url'       :'/api/blockschedule/',
            'method'    : 'GET',
            'params'    : {'date' : $scope.queryDate}
        }).success(function(data) {
                $scope.slots= data;
            });
    };

    var isLastBlockDate = function() {
        return $scope.currdate == $scope.lastDate;
    };

    var isFirstBlockDate = function() {
        return $scope.currdate == $scope.firstDate;
    };

    var previousBlockDate = function() {
        var d1 = new Date($scope.currdate);
        if (d1 == $scope.firstDate) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()-7);
        while (d2 != $scope.lastDate && $scope.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d3.getDate()-7);
        }

        return d2;
    };

    var nextBlockDate = function() {
        var d1 = new Date($scope.currdate);
        if (d1 == $scope.lastDate) {
            return d1;
        }
        var d2 = new Date(d1.getFullYear(), d1.getMonth(),d1.getDate()+7);
        while (d2 != $scope.lastDate && $scope.blocksched[d2] == 1) {
            d2 = new Date(d2.getFullYear(), d2.getMonth(),d3.getDate()+7);
        }

        return d2;
    };

    $scope.isHoldout = function() {

    };

    $scope.previous = function() {
        $scope.queryDate = previousBlockDate();
        updateAll();
    };

    $scope.next = function() {
        $scope.queryDate = nextBlockDate();
        updateAll();
    };

    updateAll();
});


