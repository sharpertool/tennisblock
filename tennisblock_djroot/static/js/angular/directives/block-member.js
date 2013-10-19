/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockMember',['Members','$q',
    function(Members,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/templates/block-member.html',
            //transclude: true,
            replace: false,
            scope: {
                member : '='
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockMember");

                var attrs = ['first','last','gender','ntrp','microntrp','phone','email'];

                $scope.memberChanged = function(member) {
                    var changed = false;
                    var m = $scope.member;
                    _.each(attrs,function(attr) {
                        changed = changed || m[attr] != m.original[attr];
                    });
                    m.changed = changed;
                    return changed;
                }

                $scope.memberFieldChanged = function(member,field) {
                    return member[field] != member.original[field];
                }

                $scope.updateMember = function(member) {
                    console.log("Updating " + member.first + " " + member.last);
                    var mdef = $q.defer();
                    Members.save({},{'member':member},function() {
                        mdef.resolve();
                    });
                    mdef.promise.then(function() {
                        Members.get({id:member.id},function(data) {
                            var m = $scope.member;
                            delete m.original;
                            m.original = JSON.parse(JSON.stringify(m));
                        });
                    });



                };
            }
        };
    }
]);

tennisblockapp.directive('blockMemberItem',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/templates/block-member-item.html',
            //transclude: true,
            replace: true,
            scope: {
                   field : '@',
                   member : '='
            },
            link: function($scope,$element,$attrs) {
                console.log("Link blockMemberItem");

                $scope.isChanged = function() {
                    var f = $scope.field;
                    var m = $scope.member;
                    return m.original[f] != m[f];
                }
            }
        };
    }
]);
