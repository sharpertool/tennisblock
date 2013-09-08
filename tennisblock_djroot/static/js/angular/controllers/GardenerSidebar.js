/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:46 PM
 */

app.controller('GardenerSidebar', function($scope,$http) {
    $http.get('/dapi/gardeners/sidebar').success(function(data) {
        $scope.sidebar = data;
    })
});


