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
                        if (response.status === 401) {
                            $location.path("/login");
                        }
                        if (response.status === 403) {
                            notifier.warning("Sorry, you're not allowed to do this");
                        }
                        return $q.reject(response);
                    }
                };
            });

            $stateProvider.
            state('site', {
                'abstract': true,
                templateUrl: partialsUrl + 'base.html',
                resolve: {
                    auth: ['auth',
                        function(auth) {
                            return auth.authorize();
                        }
                    ]
                }
            }).
            state('login', {
                url: '/login',
                templateUrl: partialsUrl + 'auth/login.html',
                controller: 'auth.LoginCtrl',
                data: {
                    access: 'ignore'
                }
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
            state('messages', {
                templateUrl: partialsUrl + 'messages/base.html',
                parent: 'site'
            }).
            state('messages.list', {
                url: '/messages',
                templateUrl: partialsUrl + 'messages/list.html',
                controller: 'messages.ListCtrl',
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
            state('amenities.detail', {
                url: '/amenities/:id',
                templateUrl: partialsUrl + 'amenities/detail.html',
                controller: 'amenities.DetailCtrl'
            }).
            state('amenities.newBooking', {
                url: '/amenities/:id/bookings/new',
                templateUrl: partialsUrl + 'amenities/bookingForm.html',
                controller: 'amenities.NewBookingCtrl'
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
                url: '/storage/new',
                templateUrl: partialsUrl + 'storage/itemForm.html',
                controller: 'storage.NewItemCtrl'
            }).
            state('storage.editItem', {
                url: '/storage/edit/:id',
                templateUrl: partialsUrl + 'storage/itemForm.html',
                controller: 'storage.EditItemCtrl'
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
            state('parking.edit', {
                url: '/parking/edit/:id',
                templateUrl: partialsUrl + 'parking/vehicleForm.html',
                controller: 'parking.EditCtrl'
            }).
            state('contacts', {
                templateUrl: partialsUrl + 'documents/base.html',
                parent: 'site'
            }).
            state('contacts.list', {
                url: '/contacts',
                templateUrl: partialsUrl + 'contacts/list.html',
                controller: 'contacts.ListCtrl'
            }).
            state('apartment', {
                url: '/apartment',
                parent: 'site',
                templateUrl: partialsUrl + 'apartment.html',
                controller: 'ApartmentCtrl'
            });

            $urlRouterProvider.otherwise('/notices');
        }
    ]);
}());
