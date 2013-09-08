'use strict';

// Declare app level module which depends on filters, and services
var app = angular.module('featuredgardeners', []);


app.controller('fgCtrl', function($scope) {
    $scope.ctrlFlavor = "blackberry";
    $scope.username = 'kutenai';
    $scope.callHome=function(message) {
        alert(message);
    }
});



// Publish our messages for the list template
function ListController($scope) {
    $scope.messages = messages;
}
// Get the message id from the route (parsed from the URL) and use it to
// find the right message object.
function DetailController($scope, $routeParams) {
    $scope.message = messages[$routeParams.id];
}

app.controller('niftyController', function($scope,$http) {
    $scope.ctrlFlavor = "nifty iPhone";
    $scope.username = 'kutenai';
    $scope.callHome=function(message) {
        alert(message);
    }
    $scope.messages = $http.get('/dapi/messages').success(function(data) {
        $scope.messages = data;
    })
    //$scope.messages = messages;
});

app.controller('niftyDetails', function($scope,$http,$routeParams) {
    $scope.ctrlFlavor = "nifty iPhone";
    $scope.username = 'kutenai';
    $scope.callHome=function(message) {
        alert(message);
    }
    $scope.messages = $http.get('/dapi/messages/'+$routeParams.id).success(function(data) {
        $scope.message = data;
    })
});

app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            controller: 'niftyController',
            templateUrl: '../partials/nifty_list.html'
        })
        .when('/nifty/:id', {
            controller: 'niftyDetails',
            templateUrl: '../partials/nifty_detail.html'
        })
        .otherwise({controller: 'fgCtrl' });
});

app.controller('dlgCtrl', function($scope) {
    $scope.username = 'kutenai';
});

app.directive('dialog', function() {
    return {
        restrict: 'E',
        scope: {
               title: '@',
               onOk: '&',
               onCancel: '&',
               visible: '='
        },
        transclude: true,
        replace: true,
        template: '<div ng-show="visible">' +
                    '<h3>{{title}}</h3>' +
                    '<div class="body" ng-transclude></div>' +
                    '<div class="footer">' +
                        '<button ng-click="onOk()">Save changes</button>' +
                      '<button ng-click="onCancel()">Close</button>' +
                    '</div>' +
                  '</div>'
    }

})

app.directive('drink', function() {
    return {
        scope: {
               flavor:"="
        },
        template: '<input type="text" mg-model="flavor">'
    }

});

app.directive('phone', function() {
    return {
        scope: {
            dial:"&"
        },
        template: '<input type="text" ng-model="value">'
            + '<div class="btn" ng-click="dial({message:value})">Call Home!</div>'
    }

});

app.directive("superhero", function() {
    return {
        restrict: "E",
        scope: {},

        controller: function($scope) {
            $scope.abilities = [];

            this.addStrength = function() {
                $scope.abilities.push("strength");
            }

            this.addSpeed = function() {
                $scope.abilities.push("speed");
            }

            this.addFlight = function() {
                $scope.abilities.push("flight");
            }
        },

        link: function(scope,element) {
            element.addClass("btn btn-danger btn-large");
            element.bind("mouseenter", function() {
                console.log(scope.abilities);
            })
        }
    }
})

app.directive("strength", function() {
    return {
        require: "superhero",
        link: function(scope,element, attrs,superheroCtrl) {
            superheroCtrl.addStrength();
        }
    }
})

app.directive("speed", function() {
    return {
        require: "superhero",
        link: function(scope,element, attrs,superheroCtrl) {
            superheroCtrl.addSpeed();
        }
    }
})

app.directive("flight", function() {
    return {
        require: "superhero",
        link: function(scope,element, attrs,superheroCtrl) {
            superheroCtrl.addFlight();
        }
    }
})

app.controller('ChoreCtrl', function($scope) {
    $scope.logChore = function(chore) {
        alert(chore + " is done!");
    }
});


app.directive("kid", function() {
    return {
        restrict: "E",
        scope: {
           done:"&"
        },
        template: '<input type="text" ng-model="chore">' +
                        ' {{chore}}' +
                         ' <div class="btn btn-success" ng-click="done({chore:chore})">I\'m done!</div>'
    }
})
