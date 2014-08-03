(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', ['$scope', '$state',
        function($scope, $state) {
            $scope.$on('$stateChangeStart', function(event, toState) {
                if (toState.url === '/login') {
                    return;
                }
                // if(!Auth.authorize(toState.data.access))...
                event.preventDefault();
                // add alert "You must be logged in...."
                $state.go('login');
            });
        }
    ]);
}());
