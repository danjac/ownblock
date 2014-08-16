(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', [
        '$scope',
        '$timeout',
        '$state',
        'auth',
        'notifier',
        function($scope, $timeout, $state, auth, notifier) {

            $scope.auth = auth;
            $scope.notifier = notifier;

            $scope.$on('Notifier.new', function(event, notification) {
                $timeout(function() {
                    notifier.remove(notification);
                }, 3000);

            });

            $scope.$on('$stateChangeStart', function() {
                console.log("stateChangeStart")
                auth.authorize();
            });

            $scope.logout = function() {
                auth.logout().then(function() {
                    $state.go('login');
                });
            };


        }
    ]).controller('ApartmentCtrl', ['$scope', '$window', 'api', 'auth',
        function($scope, $window, api, auth) {

            $scope.building = $scope.auth.user.building;

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
                    point = new OL.LonLat($scope.building.longitude,
                        $scope.building.latitude).transform(fromProjection, toProjection),
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

            $scope.apartments = [];
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
                angular.forEach($scope.apartments, function(apt) {
                    if (apt.id === auth.user.apartment.id) {
                        $scope.apartment = apt;
                        $scope.apartment_name = "My apartment";
                        return;
                    }
                });
            });
            $scope.tabs = {
                building: {
                    active: true
                },
                apartment: {
                    active: false
                },
                apartments: {
                    active: false
                }
            };
            $scope.getApartment = function(id) {
                angular.forEach($scope.apartments, function(apt) {
                    if (apt.id === id) {
                        $scope.apartment = apt;
                        $scope.apartment_name = apt.id === auth.user.apartment.id ? 'My apartment' : 'Apartment ' + apt.number + "/" + apt.floor;
                        $scope.tabs.apartment.active = true;
                        return;
                    }
                });
            };
        }
    ]).controller('residents.ListCtrl', ['$scope', 'api', 'auth',
        function($scope, api, auth) {
            $scope.residents = [];
            $scope.user = auth.user;
            api.Resident.query().$promise.then(function(response) {
                $scope.residents = response;
            });
        }
    ]).controller('amenities.ListCtrl', ['$scope', 'api',
        function($scope, api) {
            $scope.amenities = [];
            api.Amenity.query().$promise.then(function(response) {
                $scope.amenities = response;
            });
        }

    ]).controller('amenities.NewBookingCtrl', ['$scope', '$state', '$stateParams', 'api',
        function($scope, $state, $stateParams, api) {
            api.Amenity.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                $scope.booking = new api.Booking({
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
    ]).controller('amenities.DetailCtrl', ['$scope',
        '$window',
        '$stateParams',
        'api',
        'notifier',
        'auth',
        function($scope, $window, $stateParams, api, notifier, auth) {
            var bookings = [];
            $scope.eventSources = [bookings];

            api.Amenity.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                $scope.bookings = [];

                angular.forEach($scope.amenity.booking_set, function(booking, counter) {
                    var reservedFrom = new Date(booking.reserved_from),
                        reservedTo = new Date(booking.reserved_to),
                        title = reservedFrom.getHours() + ":" + reservedFrom.getMinutes() +
                        " - " + reservedTo.getHours() + ":" + reservedTo.getMinutes(),
                        color = auth.user.id === booking.resident ? '#800' : '#008';

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
                if (booking.resident !== auth.user.id) {
                    return;
                }
                if (!$window.confirm("You want to cancel this booking?")) {
                    return;
                }
                api.booking.remove({
                    id: booking.id
                });
                bookings.splice(counter, 1);
                notifier.success('Your booking has been canceled');
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
    ]).controller('notices.ListCtrl', ['$scope', 'api',
        function($scope, api) {
            $scope.notices = [];
            api.Notice.query().$promise.then(function(response) {
                $scope.notices = response;
            });
        }
    ]).controller('notices.DetailCtrl', [
        '$scope',
        '$stateParams',
        '$state',
        'notifier',
        'auth',
        'api',

        function($scope, $stateParams, $state, notifier, auth, api) {
            api.Notice.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.notice = response;
            });

            $scope.auth = auth;

            $scope.deleteNotice = function() {
                $scope.notice.$delete(function() {
                    notifier.success('Your notice has been removed');
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('notices.NewCtrl', ['$scope', '$state', 'notifier', 'api',
        function($scope, $state, notifier, api) {
            $scope.notice = new api.Notice();
            $scope.save = function() {
                $scope.notice.$save(function() {
                    notifier.success('Your notice has been published');
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('messages.ListCtrl', ['$scope', 'api', 'auth',
        function($scope, api, auth) {
            $scope.receivedMessages = [];
            $scope.sentMessages = [];
            api.Message.query().$promise.then(function(response) {
                angular.forEach(response, function(message) {
                    if (message.recipient === auth.user.id) {
                        $scope.receivedMessages.push(message);
                    } else {
                        $scope.sentMessages.push(message);
                    }
                });
            });
        }
    ]).controller('messages.SendCtrl', [
        '$scope',
        '$state',
        '$stateParams',
        'api',
        'notifier',
        function($scope, $state, $stateParams, api, notifier) {
            $scope.message = new api.Message({
                recipient: $stateParams.recipient
            });
            $scope.send = function() {
                $scope.message.$save(function() {
                    notifier.success('Your message has been sent');
                    $state.go('messages.list');
                }, function(response) {});
            };
        }
    ]).controller('messages.ReplyCtrl', [
        '$scope',
        '$state',
        '$stateParams',
        'api',
        'notifier',
        function($scope, $state, $stateParams, api, notifier) {
            $scope.message = new api.Message({
                parent: $stateParams.parent
            });
            api.Message.get({
                id: $stateParams.parent
            }).$promise.then(function(response) {
                $scope.message.header = "Re: " + response.header;
                if (response.details) {
                    $scope.message.details = "> " + response.details;
                }
                $scope.message.recipient = response.sender.id;
            });
            $scope.send = function() {
                $scope.message.$save(function() {
                    notifier.success('Your message has been sent');
                    $state.go('messages.list');
                }, function(response) {});
            };
        }
    ]).controller('storage.ListCtrl', ['$scope', '$window', 'api',
        function($scope, $window, api) {

            $scope.items = [];
            api.StorageItem.query().$promise.then(function(response) {
                $scope.items = response;
            });

            $scope.deleteItem = function(item, index) {
                if (!$window.confirm('Are you sure you want to remove this item?')) {
                    return;
                }
                $scope.items.splice(index, 1);
                item.$delete();
            };
        }
    ]).controller('storage.NewItemCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            $scope.item = new api.StorageItem();
            $scope.places = [];

            api.Place.query().$promise.then(function(response) {
                $scope.places = response;
            });

            $scope.save = function() {
                $scope.item.$save(function() {
                    notifier.success('Your item has been added');
                    $state.go('storage.list');
                });
            };

        }
    ]).controller('storage.EditItemCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            api.StorageItem.get({
                id: $state.params.id
            }, function(response) {
                $scope.item = response;
            });

            $scope.places = [];

            api.Place.query().$promise.then(function(response) {
                $scope.places = response;
            });

            $scope.save = function() {
                $scope.item.$update(function() {
                    notifier.success('Your item has been updated');
                    $state.go('storage.list');
                });
            };
        }
    ]).controller('contacts.ListCtrl', ['$scope', 'api',
        function($scope, api) {
            $scope.contacts = [];
            api.Contact.query().$promise.then(function(response) {
                $scope.contacts = response;
            });

        }
    ]).controller('documents.ListCtrl', ['$scope', 'api',
        function($scope, api) {
            $scope.documents = [];
            api.Document.query().$promise.then(function(response) {
                $scope.documents = response;
            });

        }
    ]).controller('parking.ListCtrl', ['$scope', '$window', 'api', 'notifier',
        function($scope, $window, api, notifier) {
            $scope.vehicles = [];
            api.Vehicle.query().$promise.then(function(response) {
                $scope.vehicles = response;
            });

            $scope.deleteVehicle = function(vehicle, index) {
                if (!$window.confirm('Are you sure you want to remove this vehicle?')) {
                    return;
                }
                vehicle.$delete(function() {
                    notifier.success('Your vehicle has been removed');
                });
                $scope.vehicles.splice(index, 1);
            };
        }
    ]).controller('parking.NewCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.vehicle = new api.Vehicle();
            $scope.save = function() {
                $scope.vehicle.$save(function() {
                    notifier.success('Your vehicle has been added');
                    $state.go('parking.list');
                });
            };
        }
    ]).controller('parking.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Vehicle.get({
                id: $state.params.id
            }, function(response) {
                $scope.vehicle = response;
            });
            $scope.save = function() {
                $scope.vehicle.$update(function() {
                    notifier.success('Your vehicle has been updated');
                    $state.go('parking.list');
                });
            };
        }
    ]).controller('auth.LoginCtrl', [
        '$scope',
        'auth',
        'notifier',
        function($scope, auth, notifier) {
            $scope.creds = {};
            $scope.login = function() {
                // Tbd: move this to auth service
                auth.login($scope.creds).then(function() {
                    notifier.success('Welcome back, ' + auth.user.first_name);
                });
            };
        }
    ]);
}());
