(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', ['$scope', '$state', 'Session', 'Auth',
        function($scope, $state, Session, Auth) {

            $scope.session = Session;

            Auth.get().$promise.then(function(response) {
                Session.user = response;
                Session.loggedIn = Session.user !== undefined;
                // set this up once we've authenticated
                $scope.$on('$stateChangeStart', function(event, toState) {
                    var access = toState.data ? toState.data.access : undefined;
                    if (access === 'ignore') {
                        return;
                    }
                    if (!Session.authorize(access)) {
                        event.preventDefault();
                        $state.go('login');
                    }
                });
                $state.go('notices.list');

            }).catch(function() {
                $state.go('login');
            });

            $scope.logout = function() {
                Auth.remove({}, function() {
                    Session.user = undefined;
                    Session.loggedIn = false;
                    $state.go('login');
                });
            };

        }
    ]).
    controller('ApartmentCtrl', ['$scope', '$window', 'Session',
        function($scope, $window, Session) {
            function generateMap() {
                var OL = $window.OpenLayers,
                    map = new OL.Map("map", {
                        controls: [new OL.Control.Navigation(),
                            new OL.Control.PanZoomBar(),
                            new OL.Control.ScaleLine(),
                            new OL.Control.MousePosition(),
                            new OL.Control.Permalink(),
                            new OL.Control.Attribution()
                        ],
                        maxExtent: new OL.Bounds(-180, -90, 180, 90),
                        displayProjection: new OL.Projection("EPSG:4326"),
                        maxResolution: 'auto'
                    }),
                    fromProjection = new OL.Projection("EPSG:4326"), // Transform from WGS 1984
                    toProjection = new OL.Projection("EPSG:900913"), // to Spherical Mercator Projection
                    layer = new OL.Layer.OSM(),
                    point = new OL.LonLat(Session.user.building.longitude,
                        Session.user.building.latitude).transform(fromProjection, toProjection),
                    markers = new OL.Layer.Markers('Markers'),
                    size = new OL.Size(21, 25),
                    offset = new OL.Pixel(-(size.w / 2), -size.h),
                    icon = new OL.Icon('http://www.openlayers.org/dev/img/marker.png', size, offset);
                map.addLayer(layer);
                map.addLayer(markers);
                map.setCenter(point, 15);
                markers.addMarker(new OL.Marker(point, icon));
            }
            generateMap();
            $scope.building = Session.user.building;
        }
    ]).
    controller('residents.ListCtrl', ['$scope', 'Resident', 'Session',
        function($scope, Resident, Session) {
            $scope.residents = [];
            $scope.user = Session.user;
            Resident.query().$promise.then(function(response) {
                $scope.residents = response;
            });
        }
    ]).
    controller('amenities.ListCtrl', ['$scope', 'Amenity',
        function($scope, Amenity) {
            $scope.amenities = [];
            Amenity.query().$promise.then(function(response) {
                $scope.amenities = response;
            });
        }

    ]).
    controller('amenities.NewBookingCtrl', ['$scope', '$state', '$stateParams', 'Amenity', 'Booking',
        function($scope, $state, $stateParams, Amenity, Booking) {
            Amenity.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                $scope.booking = new Booking({
                    amenity: $scope.amenity.id,
                    reserved_from: new Date(),
                    reserved_to: new Date()
                });
            });

            $scope.timepickerOptions = {
                showMeridian: false,
                disabled: false
            };
            $scope.datepickerOptions = {
                disabled: false
            };

            $scope.save = function() {
                $scope.booking.$save(function() {
                    // alert this
                    $state.go('amenities.detail', {
                        id: $stateParams.id
                    });
                }, function(response) {
                    console.log(response);
                });
            };
        }
    ]).
    controller('amenities.DetailCtrl', ['$scope',
        '$window',
        '$stateParams',
        'Amenity',
        'Booking',
        'Session',
        function($scope, $window, $stateParams, Amenity, Booking, Session) {
            var bookings = [];
            $scope.eventSources = [bookings];

            Amenity.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                $scope.bookings = [];

                angular.forEach($scope.amenity.booking_set, function(booking, counter) {
                    var reservedFrom = new Date(booking.reserved_from),
                        reservedTo = new Date(booking.reserved_to),
                        title = reservedFrom.getHours() + ":" + reservedFrom.getMinutes() +
                        " - " + reservedTo.getHours() + ":" + reservedTo.getMinutes(),
                        color = Session.user.id === booking.resident ? '#800' : '#008';

                    bookings.push({
                        start: reservedFrom,
                        end: reservedTo,
                        color: color,
                        title: title,
                        data: booking,
                        index: counter
                    });
                });
            });

            function cancelBooking(booking, counter) {
                if (booking.resident !== Session.user.id) {
                    return;
                }
                if (!$window.confirm("You want to cancel this booking?")) {
                    return;
                }
                Booking.remove({
                    id: booking.id
                });
                bookings.splice(counter, 1);
            }

            $scope.uiConfig = {
                calendar: {
                    height: 450,
                    editable: false,
                    header: {
                        left: 'basicDay basicWeek month',
                        center: 'title',
                        right: 'today prev,next'
                    },
                    eventClick: function(calEvent) {
                        cancelBooking(calEvent.data, calEvent.index);
                    }
                }
            };

        }
    ]).controller('notices.ListCtrl', ['$scope', 'Notice',
        function($scope, Notice) {
            $scope.notices = [];
            Notice.query().$promise.then(function(response) {
                $scope.notices = response;
            });
        }
    ]).controller('notices.DetailCtrl', ['$scope', '$stateParams', '$state', 'Notice',

        function($scope, $stateParams, $state, Notice) {
            Notice.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.notice = response;
            });

            $scope.deleteNotice = function() {
                $scope.notice.$delete(function() {
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('notices.NewCtrl', ['$scope', '$state', 'Notice',
        function($scope, $state, Notice) {
            $scope.notice = new Notice();
            $scope.save = function() {
                $scope.notice.$save(function() {
                    // fire alert
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('auth.LoginCtrl', ['$scope', '$state', '$window', 'Auth', 'Session',
        function($scope, $state, $window, Auth, Session) {
            $scope.creds = {};
            $scope.login = function() {
                Auth.login($scope.creds).$promise.then(function(response) {
                    if (response.role === 'admin') {
                        $window.location.href = '/admin/';
                    }
                    Session.user = response;
                    Session.loggedIn = true;
                    $state.go("notices.list");
                });
            };
        }
    ]);
}());
