/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

app.controller('LatestBuzz', function($scope,$routeParams, $http) {
    $http.get('/dapi/buzz/').success(function(data) {
        $scope.buzzitems = data;
    })
});

