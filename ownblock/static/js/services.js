(function() {
    'use strict';
    angular.module('ownblock.services', []).
    service('auth', [

        function() {

            return {
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
                sync: function(response) {
                    this.user = response;
                },
                update: function(response) {
                    this.user.first_name = response.first_name;
                    this.user.last_name = response.last_name;
                    this.user.email = response.email;
                    this.user.full_name = response.full_name;
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
    ]).factory('paginator', ['$filter',
        function($filter) {

            var Paginator = function(items, maxSize) {
                this.maxSize = maxSize || 10;
                this.refresh(items);
            };

            Paginator.prototype.change = function() {
                var offset = (this.page - 1) * this.maxSize;
                this.currentItems = this.filteredItems.slice(offset, offset + this.maxSize);
                this.isEmpty = this.currentItems.length === 0;
            };

            Paginator.prototype.refresh = function(items) {
                this.items = this.filteredItems = items || [];
                this.total = this.items.length;
                this.page = 1;
                this.change();
            };

            Paginator.prototype.filter = function(value) {
                if (value) {
                    this.filteredItems = $filter('filter')(this.items, value);
                } else {
                    this.filteredItems = this.items;
                }
                this.total = this.filteredItems.length;
                this.change();
            };

            Paginator.prototype.remove = function(index) {
                this.items.splice(index, 1);
                this.items.total = this.items.length;
                this.change();
            };

            return function(items, maxSize) {
                return new Paginator(items, maxSize);
            };

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
                Complaint: makeEndpoint('/api/complaints/complaints/:id'),
                Ticket: makeEndpoint('/api/tickets/tickets/:id'),
                Apartment: makeEndpoint('/api/buildings/apartments/:id', {
                    addResident: {
                        url: '/api/buildings/apartments/:id/add_resident',
                        method: 'POST'
                    }
                }),
                Building: makeEndpoint('/api/buildings/buildings/:id'),
                Auth: $resource('/api/users/auth/', {}, {
                    update: {
                        method: 'PUT'
                    },
                    changePassword: {
                        method: 'PATCH'
                    }
                })
            };
        }
    ]);
}());
