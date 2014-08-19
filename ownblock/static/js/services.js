(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('auth', [
        '$q',
        '$window',
        'api',
        function($q, $window, api) {
            var storageKey = 'auth.user',
                storage = $window.localStorage;

            return {
                storageKey: 'auth.user',
                authenticate: function() {
                    if (this.isAuthenticated) {
                        return true;
                    }
                    // check local storage 
                    var user = storage.getItem(storageKey);
                    if (user === null) { // user not in local storage
                        return false;
                    }
                    this.user = JSON.parse(user);
                    this.isAuthenticated = true;
                    return true;
                },
                authorize: function(state) {
                    var data = state.data || {},
                        access = data.access || null;

                    return this.hasRole(access);
                },
                hasRole: function(access) {
                    if (!access) {
                        return true;
                    }
                    return (this.user && this.user.role === access);
                },
                login: function(response) {
                    this.user = response;
                    this.isAuthenticated = true;
                    storage.setItem(storageKey, JSON.stringify(this.user));
                }
            };
        }
    ]).factory('notifier', ['$rootScope',
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
            Notifier.prototype.warning = function(msg) {
                this.notify('warning', msg);
            };
            Notifier.prototype.info = function(msg) {
                this.notify('info', msg);
            };
            Notifier.prototype.danger = function(msg) {
                this.notify('danger', msg);
            };
            return new Notifier();
        }
    ]).service('api', ['$resource',
        function($resource) {

            function makeEndpoint(url, actions) {
                if (!angular.isDefined(actions)) {
                    actions = {
                        update: {
                            method: 'PUT'
                        }
                    };
                }
                return $resource(url, {
                    id: '@id',
                }, actions);
            }

            return {
                Notice: makeEndpoint('/api/notices/notices/:id'),
                Message: makeEndpoint('/api/messages/messages/:id'),
                Resident: makeEndpoint('/api/users/people/:id'),
                Amenity: makeEndpoint('/api/amenities/items/:id'),
                Booking: makeEndpoint('/api/amenities/bookings/:id'),
                Place: makeEndpoint('/api/storage/places/:id'),
                Document: makeEndpoint('/api/documents/documents/:id'),
                Contact: makeEndpoint('/api/contacts/contacts/:id'),
                Vehicle: makeEndpoint('/api/parking/vehicles/:id'),
                StorageItem: makeEndpoint('/api/storage/items/:id'),
                Apartment: makeEndpoint('/api/buildings/apartments/:id', {
                    addResident: {
                        url: '/api/buildings/apartments/:id/add_resident',
                        method: 'POST'
                    }
                }),
                Building: makeEndpoint('/api/buildings/buildings/:id'),
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
