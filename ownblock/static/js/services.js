(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('auth', ['$q', '$state', '$window', 'api',
        function($q, $state, $window, api) {
            return {
                user: undefined,
                authorize: function(access) {
                    var deferred = $q.defer(),
                        self = this;

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
                    if (!angular.isDefined(this.user)) {
                        return false;
                    }
                    if (!access) {
                        return true;
                    }
                    return (access === this.user.role);
                },
                login: function(creds) {
                    var self = this;
                    api.auth.login(creds).$promise.then(function(response) {
                        if (response.role === 'admin') {
                            $window.location.href = '/admin/';
                        }
                        self.user = response;
                        self.loggedIn = true;
                        // tbd: set based on state params etc
                        $state.go("notices.list");
                    });

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
            return {
                notice: $resource('/api/notices/notices/:id', {
                    id: '@id'
                }),
                message: $resource('/api/messages/messages/:id', {
                    id: '@id'
                }),
                resident: $resource('/api/users/people/:id', {
                    id: '@id'
                }),
                amenity: $resource('/api/amenities/items/:id', {
                    id: '@id'
                }),
                booking: $resource('/api/amenities/bookings/:id', {
                    id: '@id'
                }),
                apartment: $resource('/api/buildings/apartments/:id', {
                    id: '@id'
                }),
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
