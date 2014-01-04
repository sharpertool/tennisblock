/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockMembers',['Members','$q',
    function(Members,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            controller: 'MembersController',
            terminal: false,
            templateUrl: '/static/templates/block-members.html',
            //transclude: true,
            replace: false,
            scope: false,
            link: function($scope,$element,$attributes,ctrl) {
                console.log("Link blockMembers");

                $scope.memberinfo = {
                    headings : ['First','Last','Gender', 'NTRP', 'uNTRP','email','phone','blockmember']
                };
                $scope.members = {
                    allmembers : []
                };

                ctrl.registerMembers($scope.members);

                var updateMembers = function(members) {
                    _.each(members,function(m) {
                        m.original = JSON.parse(JSON.stringify(m));
                        m.new = false;
                        m.changed = false;
                    });
                    $scope.members.allmembers = members;
                };

                var update = function() {

                    var mdef = $q.defer();
                    Members.query({},function(data) {
                        mdef.resolve(data);
                    });

                    $q.all([mdef.promise]).then(function(results) {
                        console.log("All calls done");
                        updateMembers(results[0]);
                    });
                };

                update();

                $scope.addNewMember = function() {
                    var newMember = {
                        'first'  : 'Rod' , 'last' : 'Rocks',
                        'gender' : 'M',
                        'ntrp' : 3.0, 'microntrp' : 3.0,
                        'email' : 'rod@yahoo.com', 'phone' : '(208) 857-3809',
                        'new' : true,
                        'changed' : false
                    };

                    ctrl.addNewMember(newMember);
                    //$scope.members.allmembers.push(newMember)
                };
            }
        };
    }
]);

