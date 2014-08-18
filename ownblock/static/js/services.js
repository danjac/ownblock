(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('auth', [
        '$q',
        '$window',
        '$state',
        '$stateParams',
        'api',
        function($q, $window, $state, $stateParams, api) {
            return {

                authenticate: function() {
                    var deferred = $q.defer(),
                        self = this;

                    if (self.isAuthenticated) {
                        if (self.loggedIn) {
                            deferred.resolve(self);
                        } else {
                            deferred.reject(self);
                        }
                    } else {
                        api.Auth.get().$promise.then(function(response) {

                            self.user = response;
                            self.loggedIn = true;
                            self.isAuthenticated = true;
                            deferred.resolve(self);

                        }, function() {

                            self.user = undefined;
                            self.loggedIn = false;
                            self.isAuthenticated = true;
                            deferred.reject(self);
                        });
                    }
                    return deferred.promise;
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
                    return (this.loggedIn && this.user && this.user.role === access);
                },
                login: function(creds) {
                    var self = this,
                        defaultView = 'notices.list',
                        deferred = $q.defer();
                    api.Auth.login(creds).$promise.then(function(response) {

                        self.user = response;
                        self.loggedIn = true;
                        self.isAuthenticated = true;
                        $window.sessionStorage.setItem('auth.user', self.user);

                        if (angular.isDefined(self.returnToState) && self.returnToState.name) {
                            $state.transitionTo(self.returnToState.name, self.returnToState.params);
                            self.returnToState = undefined;
                        } else {
                            $state.transitionTo(defaultView);
                        }
                        deferred.resolve(self);
                    });
                    return deferred.promise;

                },
                logout: function() {
                    var deferred = $q.defer(),
                        self = this;

                    api.Auth.remove({}, function() {
                        self.user = undefined;
                        self.loggedIn = false;
                        self.isAuthenticated = false;
                        $window.sessionStorage.removeItem('auth.user');
                        deferred.resolve(true);
                    });
                    return deferred.promise;
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
