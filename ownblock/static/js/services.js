(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('Session', function() {
        return {
            user: undefined,
            authorize: function(access) {
                console.log(this.user);
                if (!this.user) {
                    return false;
                }
                if (!access) {
                    return true;
                }
                return (access === this.user.role);
            }
        };
    }).
    factory('Auth', ['$resource',
        function($resource) {
            return $resource('/api/auth', {}, {
                login: {
                    method: 'POST'
                },
                logout: {
                    method: 'DELETE'
                }
            });
        }
    ]);
}());
