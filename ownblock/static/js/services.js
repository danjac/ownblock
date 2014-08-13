(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('Session', function() {
        return {
            user: undefined,
            authorize: function(access) {
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
    factory('Notice', ['$resource',
        function($resource) {
            return $resource('/api/notices/notices/:id', {
                id: '@id'
            });
        }
    ]).
    factory('Resident', ['$resource',
        function($resource) {
            return $resource('/api/users/residents/:id', {
                id: '@id'
            });
        }
    ]).
    factory('Amenity', ['$resource',
        function($resource) {
            return $resource('/api/amenities/amenities/:id', {
                id: '@id'
            });
        }
    ]).
    factory('Booking', ['$resource',
        function($resource) {
            return $resource('/api/amenities/bookings/:id', {
                id: '@id'
            });
        }
    ]).
    factory('Auth', ['$resource',
        function($resource) {
            return $resource('/api/users/auth/', {}, {
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
