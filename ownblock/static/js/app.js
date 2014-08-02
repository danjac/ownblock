(function() {
    'use strict';
    angular.module('ownblock', [
        'ngResource',
        'ngSanitize',
        'ngCookies',
        'ui.router',
        'ui.calendar',
        'ui.bootstrap'
    ]).
    config(['$stateProvider',
        '$urlRouterProvider',
        function(
            $stateProvider,
            $urlRouterProvider) {

            $urlRouterProvider.otherwise('/notices');

            $stateProvider.
            state('notices', {
                templateUrl: '/static/partials/notices/base.html'
            }).
            state('notices.list', {
                url: '/notices',
                templateUrl: '/static/partials/notices/list.html'
            }).
            state('notices.detail', {
                url: '/notices/:id',
                templateUrl: '/static/partials/notices/detail.html'
            }).
            state('messages', {
                url: '/messages',
                templateUrl: '/static/partials/messages.html'
            }).
            state('amenities', {
                url: '/amenities',
                templateUrl: '/static/partials/amenities.html'
            }).
            state('calendar', {
                url: '/calendar',
                templateUrl: '/static/partials/calendar.html',
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
                templateUrl: '/static/partials/documents.html'
            }).
            state('apartment', {
                url: '/apartment',
                templateUrl: '/static/partials/apartment.html'
            });
        }
    ]);
}());
