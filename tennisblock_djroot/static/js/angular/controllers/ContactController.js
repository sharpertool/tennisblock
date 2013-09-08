/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 5/31/13
 * Time: 4:39 PM
 */

app.controller('ContactController', function($scope,$http) {
    $scope.master = {};
    $scope.contact = {
        'name' : "",
        'email' : "",
        'phone' : "",
        'message' : "",
        'captcha' : ""
    };
    $scope.message="Type Your Entry";

    $scope.update = function(user) {
        $scope.master= angular.copy(user);
    };

    $scope.reset = function() {
        $scope.user = angular.copy($scope.master);
    };

    $scope.submit = function(contact) {
        $http({
            'url' : '/dapi/contact/',
            'method' : 'post',

            'data' : JSON.stringify(contact),
            'headers' : {
                        'Content-type': 'application/json'
            }
        })
            .success(function(data) {
                console.log("Message sent");
                $scope.message = "Your Contact request has been sent.";
                $scope.response = data.msg;
            })
            .error(function(data, status, headers, config) {
                console.log("Message error");
                $scope.message = "Your Contact reuqest failed.";
            });
    };

});
