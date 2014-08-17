(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('auth', [
        '$q',
        '$state',
        '$stateParams',
        '$window',
        'api',
        function($q, $state, $stateParams, $window, api) {
            return {
                authorize: function(toState, toStateParams) {
                    var deferred = $q.defer(),
                        self = this,
                        access = null;

                    if (!angular.isDefined(toState)) {
                        toState = $state.current;
                    }
                    if (!angular.isDefined(toStateParams)) {
                        toStateParams = $stateParams;
                    }

                    if (toState.data) {
                        access = toState.data.access;
                    }
                    if (access !== 'ignore') {
                        self.returnToState = {
                            name: toState.name,
                            params: toState.params
                        };
                    }

                    function redirectToLogin() {
                        $state.go('login');
                    }

                    if (angular.isDefined(self.user)) {
                        if (!self.hasRole(access)) {
                            //redirectToLogin(); -> this doesn't work as we have the original view with this access
                        }
                        deferred.resolve(self);

                    } else {

                        api.Auth.get().$promise.then(function(response) {
                            self.user = response;
                            self.loggedIn = true;

                            if (!self.hasRole(access)) {
                                redirectToLogin();
                            }

                            deferred.resolve(self);

                        }, function() {

                            self.user = undefined;
                            self.loggedIn = false;
                            redirectToLogin();
                            deferred.resolve(self);

                        });
                    }

                    return deferred.promise;
                },
                hasRole: function(access) {
                    if (!access) {
                        return true;
                    }
                    if (!angular.isDefined(this.user)) {
                        return false;
                    }
                    return (access === this.user.role);
                },
                login: function(creds) {
                    var self = this,
                        defaultView = 'notices.list',
                        deferred = $q.defer();
                    api.Auth.login(creds).$promise.then(function(response) {
                        if (response.role === 'admin') {
                            $window.location.href = '/admin/';
                        }
                        self.user = response;
                        self.loggedIn = true;

                        if (angular.isDefined(self.returnToState) && self.returnToState.name) {
                            $state.go(self.returnToState.name, self.returnToState.params);
                        } else {
                            $state.go(defaultView);
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

            function makeEndpoint(url) {
                return $resource(url, {
                    id: '@id',
                }, {
                    update: {
                        method: 'PUT'
                    }
                });
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
                Apartment: makeEndpoint('/api/buildings/apartments/:id'),
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
