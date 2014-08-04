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
        '$stateProvider',
        '$urlRouterProvider',
        'staticUrl',
        function(
            $httpProvider,
            $stateProvider,
            $urlRouterProvider,
            staticUrl) {

            var partialsUrl = staticUrl + '/partials/';

            //$resourceProvider.defaults.stripTrailingSlashes = false;

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

            $urlRouterProvider.otherwise('/notices');

            $stateProvider.
            state('login', {
                url: '/login',
                templateUrl: partialsUrl + 'auth/login.html',
                controller: 'LoginCtrl'
            }).
            state('notices', {
                templateUrl: partialsUrl + 'notices/base.html'
            }).
            state('notices.list', {
                url: '/notices',
                templateUrl: partialsUrl + 'notices/list.html'
            }).
            state('notices.detail', {
                url: '/notices/:id',
                templateUrl: partialsUrl + 'notices/detail.html'
            }).
            state('messages', {
                url: '/messages',
                templateUrl: partialsUrl + 'messages.html'
            }).
            state('amenities', {
                url: '/amenities',
                templateUrl: partialsUrl + 'amenities.html'
            }).
            state('calendar', {
                url: '/calendar',
                templateUrl: partialsUrl + 'calendar.html',
                controller: function($scope) {
                    $scope.uiConfig = {
                        calendar: {
                            height: 450,
                            editable: false,
                            header: {
                                left: 'basicDay basicWeek month',
                                center: 'title',
                                right: 'today prev,next'
                            }
                        }
                    };

                    $scope.eventSources = [

                        function(start, end, callback) {
                            var items = [];
                            return callback(items);
                        }
                    ];


                }
            }).
            state('documents', {
                url: '/docs',
                templateUrl: partialsUrl + 'documents.html'
            }).
            state('apartment', {
                url: '/apartment',
                templateUrl: partialsUrl + 'apartment.html'
            });
        }
    ]);
}());
