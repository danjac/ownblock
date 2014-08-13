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
    factory('Notifier', ['$rootScope',
        function($rootScope) {
            var Notifier = function() {
                this.notifications = [];
            };
            Notifier.prototype.notify = function(type, msg) {
                var notification = {
                    type: type,
                    message: msg
                };
                $rootScope.$broadcast('Notifier.new', notification);
                this.notifications.push(notification);
            };
            Notifier.prototype.dismiss = function(index) {
                this.notifications.splice(index, 1);
            };
            Notifier.prototype.remove = function(notification) {
                var index = this.notifications.indexOf(notification);
                this.dismiss(index);
            };
            Notifier.prototype.success = function(msg) {
                this.notify('success', msg);
            };
            return new Notifier();
        }
    ]).
    service('Api', ['$resource',
        function($resource) {
            return {
                Notice: $resource('/api/notices/notices/:id', {
                    id: '@id'
                }),
                Message: $resource('/api/messages/messages/:id', {
                    id: '@id'
                }),
                Resident: $resource('/api/users/people/:id', {
                    id: '@id'
                }),
                Amenity: $resource('/api/amenities/items/:id', {
                    id: '@id'
                }),
                Booking: $resource('/api/amenities/bookings/:id', {
                    id: '@id'
                }),
                Apartment: $resource('/api/buildings/apartments/:id', {
                    id: '@id'
                }),
                Auth: $resource('/api/users/auth/', {}, {
                    login: {
                        method: 'POST'
                    },
                    logout: {
                        method: 'DELETE'
                    }
                })
            };
        }
    ]);
}());
