/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */


app.controller('Availability', function($scope,$http) {
    $scope.dates = [];
    $scope.players = [
        {'name' : 'Ed Henderson', 'avail' : [true,true,true,true]},
        {'name' : 'Vici Henderson', 'avail' : [true,true,true,true]}
    ];

    $http.get('/api/blockdates').success(function(data) {
        $scope.dates= data;
    });
    $http.get('/api/availability').success(function(data) {
        $scope.players = data;
    });

    $scope.isHoldout = function() {

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


