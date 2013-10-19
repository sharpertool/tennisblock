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
            terminal: false,
            templateUrl: '/static/js/angular/templates/block-members.html',
            //transclude: true,
            replace: false,
            scope: false,
            link: function($scope,$element,$attributes) {
                console.log("Link blockMembers");

                $scope.members = {
                    headings : ['Name', 'NTRP', 'Gender', 'uNTRP'],
                    allmembers : [
                        {
                            'first'  : 'Ed' , 'last' : 'Henderson',
                            'gender' : 'M',
                            'ntrp' : 3.5, 'microntrp' : 3.8,
                            'new' : false,
                            'changed' : false
                        },
                        {
                            'first'  : 'Vicki' , 'last' : 'Henderson',
                            'gender' : 'M',
                            'ntrp' : 3.5, 'microntrp' : 3.8,
                            'new' : false,
                            'changed' : false
                        }
                    ]
                };

                var updateMembers = function(members) {
                    _.each(members,function(m) {
                        m.new = false;
                        m.changed = false;
                    });
                    $scope.members.allmembers = members;
                };

                var update = function() {

                    var mdef = $q.defer();
                    Members.get({},function(data) {
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
                        'first'  : '' , 'last' : '',
                        'gender' : '',
                        'ntrp' : 3.0, 'microntrp' : 3.0,
                        'new' : true,
                        'changed' : false
                    };

                    $scope.members.allmembers.push(newMember)
                };
            }
        };
    }
]);

