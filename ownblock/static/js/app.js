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
        'ownblock.services'
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

            $httpProvider.interceptors.push(function($q, $location) {
                return {
                    'responseError': function(response) {
                        if (response.status === 401 || response.status === 403) {
                            $location.path("/login");
                        }
                        return $q.reject(response);
                    }
                };
            });


            $stateProvider.
            state('login', {
                url: '/login',
                templateUrl: partialsUrl + 'auth/login.html',
                controller: 'auth.LoginCtrl',
                data: {
                    access: 'ignore'
                }
            }).
            state('residents', {
                templateUrl: partialsUrl + 'residents/base.html'
            }).
            state('residents.list', {
                url: '/residents',
                templateUrl: partialsUrl + 'residents/list.html',
                controller: 'residents.ListCtrl'
            }).
            state('notices', {
                templateUrl: partialsUrl + 'notices/base.html'
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
            state('messages', {
                url: '/messages',
                templateUrl: partialsUrl + 'messages.html'
            }).
            state('amenities', {
                templateUrl: partialsUrl + 'amenities/base.html'
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
            state('documents', {
                url: '/docs',
                templateUrl: partialsUrl + 'documents.html'
            }).
            state('apartment', {
                url: '/apartment',
                templateUrl: partialsUrl + 'apartment.html',
                controller: 'ApartmentCtrl'
            });

            $urlRouterProvider.otherwise('/notices');
        }
    ]);
}());
