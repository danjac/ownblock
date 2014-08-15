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

            var partialsUrl = staticUrl + '/partials/',
                defaultBaseTemplate = '<div ui-view></div>';

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
                template: defaultBaseTemplate,
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
            state('documents', {
                url: '/docs',
                templateUrl: partialsUrl + 'documents.html'
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
