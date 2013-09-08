/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:48 PM
 */


function NurseryDetailCtrl($scope, $routeParams, Phone) {
    $scope.phone = Nursery.get({nurseryId: $routeParams.nurseryId}, function(nursery) {
        //$scope.mainImageUrl = phone.images[0];
    });

}


