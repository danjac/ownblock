(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', ['$scope', '$state', 'Session', 'Auth',
        function($scope, $state, Session, Auth) {

            $scope.loggedIn = false;
            $scope.currentUser = undefined;

            Auth.get().$promise.then(function(response) {
                Session.user = response;
                $scope.currentUser = Session.user;
                $scope.loggedIn = $scope.currentUser !== undefined;
            }).catch(function() {});

            $scope.$on('$stateChangeStart', function(event, toState) {
                if (toState.url === '/login') {
                    return;
                }
                var access = toState.data ? toState.data.access : undefined;
                if (!Session.authorize(access)) {
                    // tbd: this firest before auth is not checked - we need to 
                    // check inside here as well, if it's not already defined.
                    event.preventDefault();
                    $state.go('login');
                }
            });
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
    controller('notices.DetailCtrl', ['$scope', '$stateParams', 'Notice',

        function($scope, $stateParams, Notice) {
            Notice.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.notice = response;
            });
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
    ]).controller('auth.LoginCtrl', ['$scope', '$window', 'Auth',
        function($scope, $window, Auth) {
            $scope.creds = {};
            $scope.login = function() {
                Auth.login($scope.creds).$promise.then(function(response) {
                    if (response.role === 'admin') {
                        $window.location.href = '/admin/';
                    }
                    // Session.user = response;
                });
            };
        }
    ]);
}());
