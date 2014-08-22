(function() {
    'use strict';
    angular.module('ownblock', [
        'ngResource',
        'ngSanitize',
        'ngCookies',
        'ui.router',
        'ui.calendar',
        'ui.bootstrap',
        'ownblock.controllers',
        'ownblock.services',
        'ownblock.directives'
    ]).
    constant({
        staticUrl: '/static'
    }).
    config(['$httpProvider',
        '$resourceProvider',
        '$stateProvider',
        '$urlRouterProvider',
        'staticUrl',
        function(
            $httpProvider,
            $resourceProvider,
            $stateProvider,
            $urlRouterProvider,
            staticUrl) {

            var partialsUrl = staticUrl + '/partials/';

            $resourceProvider.defaults.stripTrailingSlashes = true;

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

            $httpProvider.interceptors.push(function($q, $location, notifier) {
                return {
                    'responseError': function(response) {
                        var warning = "Sorry, an error has occurred",
                            result = $q.reject(response);
                        switch (response.status) {
                            case 401:
                            case 403:
                                // we're out of sync with server, logout 
                                $location.path("/account/login/");
                                return result;
                            case 404:
                                $location.path("notfound");
                                return result;
                            case 400:
                                warning = "Sorry, your form appears to have some errors";
                                break;
                        }
                        if (warning) {
                            notifier.warning(warning);
                        }
                        return $q.reject(response);
                    }
                };
            });

            // handle file uploads
            $httpProvider.defaults.transformRequest = function(data, headersGetter) {

                if (data === undefined) {
                    return data;
                }

                var fd = new FormData(),
                    isFileUpload = false,
                    headers = headersGetter();

                angular.forEach(data, function(value, key) {
                    if (value instanceof FileList) {
                        isFileUpload = true;
                        if (value.length === 1) {
                            fd.append(key, value[0]);
                        } else {
                            angular.forEach(value, function(file, index) {
                                fd.append(key + "_" + index, file);
                            });
                        }
                    } else {
                        fd.append(key, value);
                    }
                });
                if (isFileUpload) {
                    headers["Content-Type"] = undefined;
                    return fd;
                }

                return JSON.stringify(data);
            };

            $stateProvider.
            state('site', {
                'abstract': true,
                templateUrl: partialsUrl + 'base.html',
                resolve: {
                    auth: ['auth',
                        function(auth) {
                            return auth;
                        }
                    ]
                }
            }).
            state('accessdenied', {
                url: '/accessdenied',
                templateUrl: partialsUrl + 'accessDenied.html',
            }).
            state('notfound', {
                url: '/notfound',
                templateUrl: partialsUrl + 'notfound.html',
            }).
            state('account', {
                templateUrl: partialsUrl + 'account/base.html',
                parent: 'site'
            }).
            state('account.edit', {
                url: '/account',
                templateUrl: partialsUrl + 'account/edit.html',
                controller: 'account.EditCtrl'
            }).
            state('account.password', {
                url: '/account/pass',
                templateUrl: partialsUrl + 'account/passwordForm.html',
                controller: 'account.ChangePasswordCtrl'
            }).
            state('residents', {
                templateUrl: partialsUrl + 'residents/base.html',
                parent: 'site'
            }).
            state('residents.list', {
                url: '/residents',
                templateUrl: partialsUrl + 'residents/list.html',
                controller: 'residents.ListCtrl'
            }).
            state('residents.new', {
                url: '/residents/new',
                templateUrl: partialsUrl + 'residents/form.html',
                controller: 'residents.NewCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('residents.edit', {
                url: '/residents/:id/edit',
                templateUrl: partialsUrl + 'residents/form.html',
                controller: 'residents.EditCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('residents.detail', {
                url: '/residents/:id',
                templateUrl: partialsUrl + 'residents/detail.html',
                controller: 'residents.DetailCtrl'
            }).
            state('messages', {
                templateUrl: partialsUrl + 'messages/base.html',
                parent: 'site'
            }).
            state('messages.list', {
                url: '/messages',
                templateUrl: partialsUrl + 'messages/list.html',
                controller: 'messages.ListCtrl',
            }).
            state('messages.detail', {
                url: '/messages/:id',
                templateUrl: partialsUrl + 'messages/detail.html',
                controller: 'messages.DetailCtrl',
            }).
            state('messages.send', {
                url: '/messages/send/:recipient',
                templateUrl: partialsUrl + 'messages/form.html',
                controller: 'messages.SendCtrl'
            }).
            state('messages.reply', {
                url: '/messages/reply/:parent',
                templateUrl: partialsUrl + 'messages/form.html',
                controller: 'messages.ReplyCtrl'
            }).
            state('notices', {
                templateUrl: partialsUrl + 'notices/base.html',
                parent: 'site'
            }).
            state('notices.list', {
                url: '/notices',
                templateUrl: partialsUrl + 'notices/list.html',
                controller: 'notices.ListCtrl'
            }).
            state('notices.new', {
                url: '/notices/new',
                templateUrl: partialsUrl + 'notices/form.html',
                controller: 'notices.NewCtrl'
            }).
            state('notices.detail', {
                url: '/notices/:id',
                templateUrl: partialsUrl + 'notices/detail.html',
                controller: 'notices.DetailCtrl'
            }).
            state('amenities', {
                templateUrl: partialsUrl + 'amenities/base.html',
                parent: 'site'
            }).
            state('amenities.list', {
                url: '/amenities',
                templateUrl: partialsUrl + 'amenities/list.html',
                controller: 'amenities.ListCtrl'
            }).
            state('amenities.newAmenity', {
                url: '/amenities/new',
                templateUrl: partialsUrl + 'amenities/amenityForm.html',
                controller: 'amenities.NewAmenityCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('amenities.edit', {
                url: '/amenities/:id/edit',
                templateUrl: partialsUrl + 'amenities/amenityForm.html',
                controller: 'amenities.EditAmenityCtrl'
            }).
            state('amenities.detail', {
                url: '/amenities/:id',
                templateUrl: partialsUrl + 'amenities/detail.html',
                controller: 'amenities.DetailCtrl'
            }).
            state('amenities.bookingDetail', {
                url: '/amenities/bookings/:id',
                templateUrl: partialsUrl + 'amenities/bookingDetail.html',
                controller: 'amenities.BookingDetailCtrl'
            }).
            state('amenities.editBooking', {
                url: '/amenities/bookings/:id/edit',
                templateUrl: partialsUrl + 'amenities/bookingForm.html',
                controller: 'amenities.EditBookingCtrl'
            }).
            state('amenities.newBooking', {
                url: '/amenities/:id/bookings/new',
                templateUrl: partialsUrl + 'amenities/bookingForm.html',
                controller: 'amenities.NewBookingCtrl',
                data: {
                    access: 'resident'
                }
            }).
            state('storage', {
                templateUrl: partialsUrl + 'storage/base.html',
                parent: 'site'
            }).
            state('storage.list', {
                url: '/storage',
                templateUrl: partialsUrl + 'storage/list.html',
                controller: 'storage.ListCtrl'
            }).
            state('storage.newItem', {
                url: '/storage/items/new',
                templateUrl: partialsUrl + 'storage/itemForm.html',
                controller: 'storage.NewItemCtrl',
                data: {
                    access: 'resident'
                }
            }).
            state('storage.newPlace', {
                url: '/storage/places/new',
                templateUrl: partialsUrl + 'storage/placeForm.html',
                controller: 'storage.NewPlaceCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('storage.itemDetail', {
                url: '/storage/:id',
                templateUrl: partialsUrl + 'storage/itemDetail.html',
                controller: 'storage.ItemDetailCtrl'
            }).
            state('storage.placeDetail', {
                url: '/storage/places/:id',
                templateUrl: partialsUrl + 'storage/placeDetail.html',
                controller: 'storage.PlaceDetailCtrl'
            }).
            state('storage.editItem', {
                url: '/storage/:id/edit',
                templateUrl: partialsUrl + 'storage/itemForm.html',
                controller: 'storage.EditItemCtrl'
            }).
            state('storage.editPlace', {
                url: '/storage/places/:id/edit',
                templateUrl: partialsUrl + 'storage/placeForm.html',
                controller: 'storage.EditPlaceCtrl'
            }).
            state('documents', {
                templateUrl: partialsUrl + 'documents/base.html',
                parent: 'site'
            }).
            state('documents.list', {
                url: '/docs',
                templateUrl: partialsUrl + 'documents/list.html',
                controller: 'documents.ListCtrl'
            }).
            state('documents.upload', {
                url: '/docs/upload',
                templateUrl: partialsUrl + 'documents/form.html',
                controller: 'documents.UploadCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('documents.detail', {
                url: '/docs/:id',
                templateUrl: partialsUrl + 'documents/detail.html',
                controller: 'documents.DetailCtrl'
            }).
            state('parking', {
                templateUrl: partialsUrl + 'parking/base.html',
                parent: 'site'
            }).
            state('parking.list', {
                url: '/parking',
                templateUrl: partialsUrl + 'parking/list.html',
                controller: 'parking.ListCtrl'
            }).
            state('parking.new', {
                url: '/parking/new',
                templateUrl: partialsUrl + 'parking/vehicleForm.html',
                controller: 'parking.NewCtrl'
            }).
            state('parking.detail', {
                url: '/parking/:id',
                templateUrl: partialsUrl + 'parking/detail.html',
                controller: 'parking.DetailCtrl'
            }).
            state('parking.edit', {
                url: '/parking/:id/edit',
                templateUrl: partialsUrl + 'parking/vehicleForm.html',
                controller: 'parking.EditCtrl'
            }).
            state('contacts', {
                templateUrl: partialsUrl + 'contacts/base.html',
                parent: 'site'
            }).
            state('contacts.list', {
                url: '/contacts',
                templateUrl: partialsUrl + 'contacts/list.html',
                controller: 'contacts.ListCtrl'
            }).
            state('contacts.new', {
                url: '/contacts/new',
                templateUrl: partialsUrl + 'contacts/form.html',
                controller: 'contacts.NewCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('contacts.detail', {
                url: '/contacts/:id',
                templateUrl: partialsUrl + 'contacts/detail.html',
                controller: 'contacts.DetailCtrl'
            }).
            state('contacts.edit', {
                url: '/contacts/:id/edit',
                templateUrl: partialsUrl + 'contacts/form.html',
                controller: 'contacts.EditCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('buildings', {
                templateUrl: partialsUrl + 'buildings/base.html',
                parent: 'site'
            }).
            state('buildings.list', {
                templateUrl: partialsUrl + 'buildings/list.html',
                controller: 'buildings.ListCtrl',
                data: {
                    acess: 'manager'
                }
            }).
            state('buildings.detail', {
                url: '/building',
                templateUrl: partialsUrl + 'buildings/detail.html',
                controller: 'buildings.DetailCtrl'
            }).
            state('buildings.apartment', {
                url: '/building/:id',
                templateUrl: partialsUrl + 'buildings/detail.html',
                controller: 'buildings.DetailCtrl'
            });

            $urlRouterProvider.otherwise('/building');
        }
    ]).run(function($rootScope, $state, auth) {

        // fetch the current user from the session. If the user is not logged in,
        // redirect to the external login page; otherwise sync user details with the 
        // application.
        $rootScope.$on('$stateChangeStart', function(event, toState) {
            if (!auth.authorize(toState)) {
                event.preventDefault();
                $state.transitionTo('accessdenied');
            }

        });

    });
}());
