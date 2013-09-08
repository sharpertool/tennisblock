/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/24/13
 * Time: 11:25 AM
 */


app.controller('CartController', function($scope) {
    $scope.items = [
        {title: 'Paint pots', quantity: 8, price: 3.95},
        {title: 'Polka dots', quantity: 17, price: 12.95},
        {title: 'Pebbles', quantity: 5, price: 6.85}
    ];

    $scope.remote = function(index) {
        $scope.items.splice(index,1);
    }
});

app.controller('StartupController', function($scope) {
    $scope.funding = {
        startingEstimate: 0.0,
        needed: 0.0,
        sellme:  "This is a test man.."
    };

    $scope.computeNeeded = function() {
        $scope.funding.needed = $scope.funding.startingEstimate * 10;
    };

    $scope.requestFunding = function() {
        window.alert("Sorry");
    };

    $scope.reset = function() {
        $scope.funding.startingEstimate = 0;
    };

    $scope.$watch('funding.startingEstimate',$scope.computeNeeded);
});

