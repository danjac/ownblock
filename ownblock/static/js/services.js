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
                            redirectToLogin();
                        }
                        deferred.resolve(self);

                    } else {

                        api.auth.get().$promise.then(function(response) {
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
                    api.auth.login(creds).$promise.then(function(response) {
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

                    api.auth.remove({}, function() {
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
                notice: makeEndpoint('/api/notices/notices/:id'),
                message: makeEndpoint('/api/messages/messages/:id'),
                resident: makeEndpoint('/api/users/people/:id'),
                amenity: makeEndpoint('/api/amenities/items/:id'),
                booking: makeEndpoint('/api/amenities/bookings/:id'),
                place: makeEndpoint('/api/storage/places/:id'),
                document: makeEndpoint('/api/documents/documents/:id'),
                contact: makeEndpoint('/api/contacts/contacts/:id'),
                vehicle: makeEndpoint('/api/parking/vehicles/:id'),
                item: makeEndpoint('/api/storage/items/:id'),
                apartment: makeEndpoint('/api/buildings/apartments/:id'),
                auth: $resource('/api/users/auth/', {}, {
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
