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
                    event.preventDefault();
                    // add alert "You must be logged in...."
                    $state.go('login');
                }
            });
        }
    ]).
    controller('LoginCtrl', ['$scope', '$window', 'Auth',
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
