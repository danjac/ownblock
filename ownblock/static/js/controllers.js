(function() {
    'use strict';
    angular.module('ownblock.controllers', []).
    controller('AppCtrl', [
        '$scope',
        '$location',
        '$timeout',
        'auth',
        'notifier',
        function($scope, $location, $timeout, auth, notifier) {

            $scope.auth = auth;
            $scope.notifier = notifier;

            $scope.init = function(user) {
                if (!user) {
                    $location.path("/account/login/");
                }
                auth.sync(user);
            };

            $scope.$on('Notifier.new', function(event, notification) {
                $timeout(function() {
                    notifier.remove(notification);
                }, 3000);

            });


        }
    ]).controller('buildings.ListCtrl', ['$scope', '$state', 'api', 'auth',
        function($scope, $state, api, auth) {
            $scope.cities = [];

            function getCity(city) {
                var rv = null;
                angular.forEach($scope.cities, function(value) {
                    if (value.name === city) {
                        rv = value;
                        return;
                    }
                });
                if (rv === null) {
                    rv = {
                        name: city,
                        buildings: []
                    };
                    $scope.cities.push(rv);
                }
                return rv;
            }
            api.Building.query().$promise.then(function(response) {
                angular.forEach(response, function(building) {
                    var city = getCity(building.city);
                    city.buildings.push(building);
                });
            });
            $scope.selectBuilding = function(building) {
                api.Building.get({
                    id: building.id
                }, function(response) {
                    auth.user.building = response;
                    $state.go('buildings.detail');
                });
            };
        }
    ]).controller('buildings.DetailCtrl', [
        '$scope',
        '$state',
        '$window',
        '$modal',
        'api',
        'auth',
        'staticUrl',
        function($scope, $state, $window, $modal, api, auth, staticUrl) {

            var apartmentId = $state.params.id;
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


            $scope.tabs = {
                building: {
                    active: true
                },
                apartments: {
                    active: false
                }
            };

            console.log(apartmentId);

            if (apartmentId) {
                $scope.tabs.apartments.active = true;
            }

            if (!apartmentId && auth.user.apartment) {
                apartmentId = auth.user.apartment.id;
            }

            api.Apartment.query().$promise.then(function(response) {

                $scope.apartments = response;
                angular.forEach($scope.apartments, function(apt) {
                    if (apartmentId && apt.id === parseInt(apartmentId, 10)) {
                        $scope.currentApartment = apt;
                        return;
                    }
                });
            });
            $scope.addResident = function(apartment) {
                var modalInstanceCtrl = function($scope, $modalInstance) {
                        $scope.resident = {};
                        $scope.cancel = function() {
                            $modalInstance.dismiss('cancel');
                        };
                        $scope.save = function() {
                            $modalInstance.close($scope.resident);
                        };
                    },
                    modalInstance = $modal.open({
                        templateUrl: staticUrl + '/partials/buildings/modalResidentForm.html',
                        controller: modalInstanceCtrl
                    });
                modalInstance.result.then(function(resident) {
                    api.Apartment.addResident({
                        id: apartment.id
                    }, resident).$promise.then(
                        function(response) {
                            $scope.apartment.user_set.push(response);
                        });
                });
            };
        }
    ]).controller('residents.ListCtrl', ['$scope', 'api', 'auth', 'paginator',
        function($scope, api, auth, paginator) {
            $scope.residents = [];
            $scope.user = auth.user;
            api.Resident.query().$promise.then(function(response) {
                $scope.residents = paginator(response);
            });
        }
    ]).controller('amenities.ListCtrl', ['$scope', '$window', 'api', 'notifier', 'paginator',
        function($scope, $window, api, notifier, paginator) {
            api.Amenity.query().$promise.then(function(response) {
                $scope.amenities = paginator(response);
            });
            $scope.deleteAmenity = function(amenity, index) {
                if (!$window.confirm('This will remove the amenity and ALL its bookings. Continue?')) {
                    return;
                }
                $scope.amenities.remove(index);
                amenity.$delete(function() {
                    notifier.success('The amenity has been removed');
                });
            };
        }
    ]).controller('amenities.NewAmenityCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.amenity = new api.Amenity({
                is_available: true
            });
            $scope.save = function() {
                $scope.amenity.$save(function() {
                    notifier.success('Amenity has been added');
                    $state.go('amenities.list');
                });
            };
        }
    ]).controller('amenities.EditAmenityCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Amenity.get({
                id: $state.params.id
            }, function(response) {
                $scope.amenity = response;
            });
            $scope.save = function() {
                $scope.amenity.$update(function() {
                    notifier.success('Amenity has been updated');
                    $state.go('amenities.list');
                });
            };
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
                }, function(response) {});
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
                if (booking.resident !== auth.user.id && !auth.hasRole('manager')) {
                    return;
                }
                if (!$window.confirm("You want to cancel this booking?")) {
                    return;
                }
                api.Booking.remove({
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
    ]).controller('notices.ListCtrl', ['$scope', '$window', 'api', 'notifier', 'paginator',
        function($scope, $window, api, notifier, paginator) {
            api.Notice.query().$promise.then(function(response) {
                angular.forEach(response, function(item) {
                    item.searchTerms = item.title + " " + item.details + item.author.full_name;
                });
                $scope.notices = paginator(response);
            });
            $scope.deleteNotice = function(notice, index) {
                if (!$window.confirm('You sure you want to delete this notice?')) {
                    return;
                }
                $scope.notices.remove(index);
                notice.$delete(function() {
                    notifier.success('Your notice has been deleted');
                });
            };
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
    ]).controller('messages.ListCtrl', ['$scope', 'api', 'auth', 'paginator',
        function($scope, api, auth, paginator) {

            api.Message.query().$promise.then(function(response) {
                var received = [],
                    sent = [];
                angular.forEach(response, function(message) {
                    message.searchTerms = message.header + " " + message.received;
                    if (message.recipient === auth.user.id) {
                        message.searchTerms += " " + message.sender.full_name;
                        received.push(message);
                    } else {
                        message.searchTerms += " " + message.recipient_detail.full_name;
                        sent.push(message);
                    }
                });
                $scope.receivedMessages = paginator(received);
                $scope.sentMessages = paginator(sent);

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
                });
            };
        }
    ]).controller('storage.ListCtrl', ['$scope', '$window', 'api', 'paginator',
        function($scope, $window, api, paginator) {

            api.StorageItem.query().$promise.then(function(response) {
                $scope.items = paginator(response);
            });

            $scope.deleteItem = function(item, index) {
                if (!$window.confirm('Are you sure you want to remove this item?')) {
                    return;
                }
                $scope.items.remove(index);
                item.$delete();
            };
        }
    ]).controller('storage.NewPlaceCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.place = new api.Place();
            $scope.save = function() {
                $scope.place.$save(function() {
                    notifier.success('The place has been saved');
                    $state.go('storage.list');
                });
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
    ]).controller('contacts.ListCtrl', ['$scope', '$window', 'api', 'notifier', 'paginator',

        function($scope, $window, api, notifier, paginator) {
            api.Contact.query().$promise.then(function(response) {
                $scope.contacts = paginator(response);
            });
            $scope.deleteContact = function(contact, index) {
                if (!$window.confirm('Are you sure')) {
                    return;
                }
                $scope.contacts.remove(index);
                contact.$delete(function() {
                    notifier.success('Contact has been removed');
                });
            };

        }
    ]).controller('contacts.DetailCtrl', ['$scope', '$state', 'api',
        function($scope, $state, api) {
            api.Contact.get({
                id: $state.params.id
            }, function(response) {
                $scope.contact = response;
            });
        }
    ]).controller('contacts.NewCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.contact = new api.Contact();
            $scope.save = function() {
                $scope.contact.$save(function() {
                    notifier.success('Your contact has been saved');
                    $state.go('contacts.list');
                });
            };
        }
    ]).controller('contacts.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Contact.get({
                id: $state.params.id
            }, function(response) {
                $scope.contact = response;
            });
            $scope.save = function() {
                $scope.contact.$update(function() {
                    notifier.success('Your contact has been saved');
                    $state.go('contacts.list');
                });
            };
        }
    ]).controller('documents.ListCtrl', ['$scope', '$window', 'api', 'notifier', 'paginator',
        function($scope, $window, api, notifier, paginator) {
            api.Document.query().$promise.then(function(response) {
                $scope.documents = paginator(response);
            });
            $scope.deleteDocument = function(doc, index) {
                if (!$window.confirm("Are you sure?")) {
                    return;
                }
                $scope.documents.remove(index);
                doc.$delete(function() {
                    notifier.success('Your document has been removed');
                });
            };

        }
    ]).controller('documents.UploadCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            $scope.document = new api.Document();
            $scope.save = function() {
                $scope.document.$save(function() {
                    notifier.success("Your document has been uploaded");
                    $state.go('documents.list');
                });
            };
        }
    ]).controller('parking.ListCtrl', ['$scope', '$window', 'api', 'notifier', 'paginator',
        function($scope, $window, api, notifier, paginator) {
            api.Vehicle.query().$promise.then(function(response) {
                angular.forEach(response, function(item) {
                    item.searchTerms = item.description + " " + item.registration_number + item.resident.full_name;
                });
                $scope.vehicles = paginator(response);
            });

            $scope.deleteVehicle = function(vehicle, index) {
                if (!$window.confirm('Are you sure you want to remove this vehicle?')) {
                    return;
                }
                vehicle.$delete(function() {
                    notifier.success('Your vehicle has been removed');
                });
                $scope.vehicles.remove(index);
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
    ]).controller('account.EditCtrl', ['$scope', 'auth', 'api', 'notifier',
        function($scope, auth, api, notifier) {
            $scope.save = function() {
                api.Auth.update(auth.user, function(response) {
                    auth.update(response);
                    notifier.success('Your account has been updated');
                });
            };
        }
    ]).controller('account.ChangePasswordCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.user = {};
            $scope.save = function() {
                api.Auth.changePassword($scope.user, function() {
                    notifier.success('Your password has been updated');
                    $state.go('account.edit');
                });
            };
        }
    ]);
}());
