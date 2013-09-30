/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */


app.controller('Availability', function($scope,$http) {
    $scope.dates = [];
    $scope.players = [];
    $scope.initialized = false;

    var updateInitialized = function() {
        if ($scope.dates.length > 0 && $scope.players.length > 0) {
            $scope.initialized = true;
        } else {
            $scope.initialized = false;
        }
    };

    $http.get('/api/blockdates').success(function(data) {
        $scope.dates= data;
        updateInitialized();
    });
    $http.get('/api/availability').success(function(data) {
        $scope.players = data;
        updateInitialized();
    });

    $scope.isHoldout = function() {

    };

    $scope.canEdit = function(player) {
        if (django.username == 'kutenai') { return true;}
        if (player.name.indexOf(django.first) != -1 && player.name.indexOf(django.last) != -1) {
            return true;
        }
        return false;
    };

    $scope.updateAvail = function(p,idx) {
        console.log('Updating for player ' + p.id + " index " + idx + " is avail?" + p.isavail[idx]);
        $http.put('/api/availability/',{
            'id' : p.id,
            'mtgidx' : idx,
            'isavail' : p.isavail[idx]
        });
    };

    $scope.computeNeeded = function() {
        //$scope.funding.needed = $scope.funding.startingEstimate * 10;
    };

    $scope.requestFunding = function() {
        window.alert("Sorry");
    };

    $scope.reset = function() {
        //$scope.funding.startingEstimate = 0;
    };

    //$scope.$watch('funding.startingEstimate',$scope.computeNeeded);
});


