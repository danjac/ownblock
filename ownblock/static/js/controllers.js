(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', ['$scope', '$state', 'Session', 'Auth',
        function($scope, $state, Session, Auth) {

            $scope.session = Session;

            Auth.get().$promise.then(function(response) {
                Session.user = response;
                Session.loggedIn = Session.user !== undefined;
                // set this up once we've authenticated
                $scope.$on('$stateChangeStart', function(event, toState) {
                    var access = toState.data ? toState.data.access : undefined;
                    if (access === 'ignore') {
                        return;
                    }
                    if (!Session.authorize(access)) {
                        event.preventDefault();
                        $state.go('login');
                    }
                });
                $state.go('notices.list');

            }).catch(function() {
                $state.go('login');
            });

            $scope.logout = function() {
                Auth.remove({}, function() {
                    Session.user = undefined;
                    Session.loggedIn = false;
                    $state.go('login');
                });
            };

        }
    ]).
    controller('notices.ListCtrl', ['$scope', 'Notice',
        function($scope, Notice) {
            $scope.notices = [];
            Notice.query().$promise.then(function(response) {
                $scope.notices = response;
            });
        }
    ]).
    controller('notices.DetailCtrl', ['$scope', '$stateParams', '$state', 'Notice',

        function($scope, $stateParams, $state, Notice) {
            Notice.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.notice = response;
            });

            $scope.deleteNotice = function() {
                $scope.notice.$delete(function() {
                    $state.go('notices.list');
                });
            };
        }
    ]).
    controller('notices.NewCtrl', ['$scope', '$state', 'Notice',
        function($scope, $state, Notice) {
            $scope.notice = new Notice();
            $scope.save = function() {
                $scope.notice.$save(function() {
                    // fire alert
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('auth.LoginCtrl', ['$scope', '$state', '$window', 'Auth', 'Session',
        function($scope, $state, $window, Auth, Session) {
            $scope.creds = {};
            $scope.login = function() {
                Auth.login($scope.creds).$promise.then(function(response) {
                    if (response.role === 'admin') {
                        $window.location.href = '/admin/';
                    }
                    Session.user = response;
                    Session.loggedIn = true;
                    $state.go("notices.list");
                });
            };
        }
    ]);
}());
