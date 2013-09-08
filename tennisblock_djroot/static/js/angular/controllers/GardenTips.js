/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

app.controller('GardenTips', function($scope,$routeParams, $http) {
    $http.get('/dapi/gardentips/10').success(function(data) {
        $scope.posts = data;
        $scope.post = $scope.posts[0];
    })

    $scope.onPost = function(idx) {
        $scope.post = $scope.posts[idx];
    };
});


