(function() {
    'use strict';
    angular.module('ownblock.controllers', [
        'ui.router',
        'ui.calendar',
        'ui.bootstrap',
        'ownblock',
        'ownblock.services'
    ]).
    controller('AppCtrl', [
        '$scope',
        '$location',
        '$state',
        '$timeout',
        'auth',
        'notifier',
        'urls',
        function($scope, $location, $state, $timeout, auth, notifier, urls) {
            $scope.auth = auth;
            $scope.notifier = notifier;

            $scope.includes = function(name) {
                return $state.includes(name);
            };

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

            $scope.menuTpl = urls.partials + 'menu.html';


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
        'urls',
        function($scope, $state, $window, $modal, api, auth, urls) {

            var apartmentId = null,
                showApartment = false;
            if ($state.params.id) {
                apartmentId = parseInt($state.params.id, 10);
                showApartment = true;
            } else if (auth.user.apartment) {
                apartmentId = auth.user.apartment;
            }
            $scope.apartmentSelector = {
                id: apartmentId
            };
            $scope.building = $scope.auth.user.building;

            var mapCreated = false;

            $scope.generateMap = function() {
                if (mapCreated) {
                    return;
                }
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
                    icon = new OL.Icon(urls.img + 'marker.png', size, offset);
                map.addLayer(layer);
                map.addLayer(markers);
                map.setCenter(point, 16);
                markers.addMarker(new OL.Marker(point, icon));
                mapCreated = true;
            };

            $scope.apartments = [];


            $scope.tabs = {
                building: {
                    active: true
                },
                apartments: {
                    active: false
                }
            };

            if (auth.hasRole('resident')) {
                $scope.tabs.building.active = false;

                $scope.tabs.timeline = {
                    active: true
                };

                var objects = {};
                $scope.timeline = [];

                api.Timeline.get(function(response) {

                    var getDateObj = function(timestamp) {

                        timestamp = new Date(timestamp);

                        var date = new Date(
                                timestamp.getFullYear(),
                                timestamp.getMonth(),
                                timestamp.getDate()),
                            obj = objects[date];

                        if (!angular.isDefined(obj)) {
                            obj = {
                                date: date,
                                notices: [],
                                messages: [],
                                documents: []
                            };
                            objects[date] = obj;
                        }

                        return obj;
                    };

                    angular.forEach(response.notices, function(notice) {
                        var dt = getDateObj(notice.created);
                        dt.notices.push(notice);
                    });

                    angular.forEach(response.messages, function(msg) {
                        var dt = getDateObj(msg.created);
                        dt.messages.push(msg);
                    });

                    angular.forEach(response.documents, function(doc) {
                        var dt = getDateObj(doc.created);
                        dt.documents.push(doc);
                    });

                    angular.forEach(objects, function(obj) {
                        $scope.timeline.push(obj);
                    });

                });
            }

            if (showApartment) {
                $scope.tabs.apartments.active = true;
            }
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
            });

            $scope.selectApartment = function() {
                if (!$scope.apartmentSelector.id) {
                    $scope.currentApartment = null;
                    return;
                }
                api.Apartment.get({
                    id: $scope.apartmentSelector.id
                }, function(response) {
                    $scope.currentApartment = response;
                });
            };

            $scope.selectApartment();

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
                        templateUrl: urls.partials + 'buildings/modalResidentForm.html',
                        controller: modalInstanceCtrl
                    });
                modalInstance.result.then(function(resident) {
                    api.Apartment.addResident({
                        id: apartment.id
                    }, resident).$promise.then(
                        function(response) {
                            $scope.currentApartment.users.push(response);
                        });
                });
            };
        }
    ]).controller('residents.ListCtrl', ['$scope', 'api', 'auth', 'paginator',
        function($scope, api, auth, paginator) {
            $scope.user = auth.user;

            $scope.paginator = paginator();
            api.Resident.query({
                residents: true
            }).$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
        }
    ]).controller('residents.NewCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.resident = new api.Resident();
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
            });
            $scope.save = function() {
                $scope.resident.$save(function() {
                    notifier.success('The resident has been added');
                    $state.go('residents.list');
                }, function(response) {
                    $scope.serverErrors = response.data;
                });
            };
            $scope.cancel = function() {
                $state.go('residents.list');
            };
        }
    ]).controller('residents.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Resident.get({
                id: $state.params.id
            }, function(response) {
                $scope.resident = response;
            });
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
            });

            $scope.save = function() {
                $scope.resident.$update(function() {
                    notifier.success('The resident has been updated');
                    $state.go('residents.detail', {
                        id: $scope.resident.id
                    });
                }, function(response) {
                    $scope.serverErrors = response.data;
                });
            };
            $scope.cancel = function() {
                $state.go('residents.detail', {
                    id: $scope.resident.id
                });
            };
        }
    ]).controller('residents.DetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Resident.get({
                id: $state.params.id
            }, function(response) {
                $scope.resident = response;
            });
            $scope.deleteUser = function() {
                $scope.resident.$delete(function() {
                    notifier.success($scope.resident.full_name + " has been removed.");
                    $state.go('residents.list');
                });
            };
        }
    ]).controller('amenities.ListCtrl', ['$scope', 'api', 'notifier', 'paginator', 'auth',
        function($scope, api, notifier, paginator, auth) {
            $scope.paginator = paginator();
            $scope.cols = ['Amenity', 'Status'];
            if (auth.hasRole('resident')) {
                $scope.cols.push('');
            }
            api.Amenity.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
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
            $scope.cancel = function() {
                $state.go('amenities.list');
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
                    $state.go('amenities.detail', {
                        id: $scope.amenity.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('amenities.detail', {
                    id: $scope.amenity.id
                });
            };
        }
    ]).controller('amenities.NewBookingCtrl', ['$scope', '$state', '$stateParams', 'api',
        function($scope, $state, $stateParams, api) {
            api.Amenity.get({
                id: $stateParams.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                var now = new Date(),
                    reservedFrom = new Date(),
                    reservedTo = new Date();

                reservedFrom.setHours(now.getHours() + 1);
                reservedTo.setHours(now.getHours() + 2);

                $scope.now = now;

                $scope.booking = new api.Booking({
                    amenity: $scope.amenity.id,
                    reserved_from: reservedFrom,
                    reserved_to: reservedTo
                });
            });

            $scope.timepickerOptions = {
                showMeridian: false,
                disabled: false
            };
            $scope.datepickerOptions = {
                disabled: false,
                dateFormat: 'dd/mm/yyyy'
            };

            $scope.save = function() {
                $scope.booking.$save(function() {
                    // alert this
                    $state.go('amenities.detail', {
                        id: $stateParams.id
                    });
                }, function(response) {
                    $scope.serverErrors = response.data;
                });
            };
        }
    ]).controller('amenities.EditBookingCtrl', ['$scope', '$state', 'api', 'notifier',

        function($scope, $state, api, notifier) {
            api.Booking.get({
                id: $state.params.id
            }, function(response) {
                $scope.now = new Date();
                $scope.booking = response;
                //                $scope.booking.reserved_to = new Date($scope.booking.reserved_to);
                //               $scope.booking.reserved_from = new Date($scope.booking.reserved_from);
            });
            $scope.save = function() {
                $scope.booking.$update(function() {
                    $state.go('amenities.detail', {
                        id: $scope.booking.amenity
                    });
                    notifier.success('Your booking has been updated');
                }, function(response) {
                    $scope.serverErrors = response.data;
                });
            };
            $scope.timepickerOptions = {
                showMeridian: false,
                disabled: false
            };
            $scope.datepickerOptions = {
                disabled: false,
                dateFormat: 'dd/mm/yyyy'
            };


        }
    ]).controller('amenities.BookingDetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Booking.get({
                id: $state.params.id
            }, function(response) {
                $scope.booking = response;
            });

            $scope.cancelBooking = function() {
                $scope.booking.$delete(function() {
                    notifier.success("The booking has been canceled");
                    $state.go('amenities.detail', {
                        id: $scope.booking.amenity
                    });
                });
            };
        }
    ]).controller('amenities.NewTicketCtrl', ['$scope',
        '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Amenity.get({
                id: $state.params.id
            }, function(response) {
                $scope.amenity = response;
                $scope.ticket = new api.Ticket({
                    amenity: $scope.amenity.id
                });
            });
            $scope.save = function() {
                $scope.ticket.$save(function() {
                    notifier.success('Thanks for reporting the issue!');
                    $state.go('amenities.detail', {
                        id: $state.params.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('amenities.detail', {
                    id: $state.params.id
                });
            };
        }
    ]).controller('amenities.DetailCtrl', ['$scope',
        '$state',
        'api',
        'auth',
        'notifier',
        'paginator',
        function($scope, $state, api, auth, notifier, paginator) {
            var bookings = [],
                today = new Date();
            $scope.paginator = paginator();
            $scope.eventSources = [bookings];
            $scope.deleteAmenity = function() {
                $scope.amenity.$delete(function() {
                    notifier.success('The amenity has been removed');
                    $state.go('amenities.list');
                });
            };

            function getColor(residentId, isPast) {
                if (isPast) {
                    return '#555';
                }
                return auth.user.id === residentId ? '#800' : '#008';
            }

            function formatTime(dt) {
                var hours = dt.getHours(),
                    mins = dt.getMinutes();
                return (hours < 10 ? "0" + hours : hours) + ":" + (mins < 10 ? "0" + mins : mins);
            }

            api.Amenity.get({
                id: $state.params.id
            }).$promise.then(function(response) {
                $scope.amenity = response;
                $scope.bookings = [];

                angular.forEach($scope.amenity.bookings, function(booking, counter) {
                    var reservedFrom = new Date(booking.reserved_from),
                        reservedTo = new Date(booking.reserved_to),
                        title = formatTime(reservedFrom) + " - " + formatTime(reservedTo),
                        isPast = reservedFrom < today,
                        color = getColor(booking.resident, isPast);

                    bookings.push({
                        start: reservedFrom,
                        end: reservedTo,
                        color: color,
                        title: title,
                        data: booking,
                        index: counter
                    });
                });

                $scope.paginator.reload($scope.amenity.tickets);
            });


            function showBooking(booking) {
                $state.go('amenities.bookingDetail', {
                    id: booking.id
                });
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
                        showBooking(calEvent.data);
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
            $scope.cancel = function() {
                $state.go('notices.list');
            };
        }
    ]).controller('notices.ListCtrl', ['$scope', 'api', 'paginator', 'urls',
        function($scope, api, paginator, urls) {
            $scope.paginator = paginator();
            api.Notice.query().$promise.then(function(response) {
                angular.forEach(response, function(item) {
                    item.searchTerms = item.title + " " + item.details + item.author.full_name;
                });
                $scope.paginator.reload(response);
            });
        }
    ]).controller('notices.DetailCtrl', [
        '$scope',
        '$state',
        'notifier',
        'api',

        function($scope, $state, notifier, api) {
            api.Notice.get({
                id: $state.params.id
            }, function(response) {
                $scope.notice = response;
            });

            $scope.deleteNotice = function() {
                $scope.notice.$delete(function() {
                    notifier.success('Your notice has been removed');
                    $state.go('notices.list');
                });
            };
        }
    ]).controller('notices.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Notice.get({
                    id: $state.params.id
                },
                function(response) {
                    $scope.notice = response;
                });

            $scope.save = function() {
                $scope.notice.$update(function() {
                    notifier.success('Your notice has been updated');
                    $state.go('notices.detail', {
                        id: $scope.notice.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('notices.detail', {
                    id: $scope.notice.id
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
    ]).controller('messages.DetailCtrl', ['$scope', '$state', 'api',
        function($scope, $state, api) {
            api.Message.get({
                id: $state.params.id
            }, function(response) {
                $scope.message = response;
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
            $scope.cancel = function() {
                $state.go('messages.list');
            };
        }
    ]).controller('messages.ReplyCtrl', [
        '$scope',
        '$state',
        'api',
        'notifier',
        function($scope, $state, api, notifier) {
            $scope.message = new api.Message({
                parent: $state.params.parent
            });
            api.Message.get({
                id: $state.params.parent
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
            $scope.cancel = function() {
                $state.go('messages.detail', {
                    id: $state.params.parent
                });
            };
        }
    ]).controller('storage.ListCtrl', ['$scope', 'api', 'paginator',
        function($scope, api, paginator) {

            $scope.paginator = paginator();
            api.StorageItem.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
            api.Place.query().$promise.then(function(response) {
                $scope.places = response;
            });

        }
    ]).controller('storage.NewPlaceCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.place = new api.Place();
            $scope.save = function() {
                $scope.place.$save(function() {
                    notifier.success('The storage area has been added');
                    $state.go('storage.list');
                });
            };
        }
    ]).controller('storage.NewItemCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            $scope.item = new api.StorageItem();
            $scope.places = [];
            $scope.editPhoto = true;
            $scope.showPhoto = false;

            api.Place.query().$promise.then(function(response) {
                $scope.places = response;
            });

            $scope.save = function() {
                $scope.item.$save(function() {
                    notifier.success('Your item has been added');
                    $state.go('storage.list');
                });
            };
            $scope.cancel = function() {

                $state.go('storage.list');
            };

        }
    ]).controller('storage.EditItemCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            $scope.editPhoto = false;
            $scope.showPhoto = false;
            $scope.places = [];

            api.StorageItem.get({
                id: $state.params.id
            }, function(response) {
                $scope.item = response;
                $scope.showPhoto = $scope.item.photo;
                $scope.editPhoto = !$scope.showPhoto;
            });


            $scope.toggleEditPhoto = function() {
                $scope.editPhoto = !$scope.editPhoto;
            };

            $scope.deletePhoto = function() {
                $scope.item.$removePhoto(function() {
                    $scope.item.photo = null;
                    $scope.showPhoto = false;
                    $scope.editPhoto = true;
                    notifier.success('Your photo has been removed');
                });
            };


            api.Place.query().$promise.then(function(response) {
                $scope.places = response;
            });

            $scope.save = function() {
                $scope.item.$update(function() {
                    notifier.success('Your item has been updated');
                    $state.go('storage.itemDetail', {
                        id: $scope.item.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('storage.itemDetail', {
                    id: $scope.item.id
                });
            };
        }
    ]).controller('storage.ItemDetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.StorageItem.get({
                id: $state.params.id
            }, function(response) {
                $scope.item = response;
            });
            $scope.deleteItem = function() {
                $scope.item.$delete(function() {
                    notifier.success('Your item has been removed');
                    $state.go('storage.list');
                });
            };
        }
    ]).controller('storage.PlaceDetailCtrl', ['$scope', '$state', 'api', 'paginator', 'notifier',
        function($scope, $state, api, paginator, notifier) {
            $scope.paginator = paginator();
            api.Place.get({
                id: $state.params.id
            }, function(response) {
                $scope.place = response;
                $scope.paginator.reload($scope.place.items);
            });
            $scope.deletePlace = function() {
                $scope.place.$delete(function() {
                    notifier.success('Storage area has been removed');
                    $state.go('storage.list');
                });
            };
        }
    ]).controller('storage.EditPlaceCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Place.get({
                id: $state.params.id
            }, function(response) {
                $scope.place = response;
            });
            $scope.save = function() {
                $scope.place.$update(function() {
                    notifier.success('The storage area has been updated');
                    $state.go('storage.placeDetail', {
                        id: $scope.place.id
                    });
                });
            };
            $scope.cancel = function() {

                $state.go('storage.placeDetail', {
                    id: $scope.place.id
                });
            };
        }
    ]).controller('contacts.ListCtrl', ['$scope', 'api', 'paginator',
        function($scope, api, paginator) {
            $scope.paginator = paginator();
            api.Contact.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
            api.Resident.query({
                managers: true
            }).$promise.then(function(response) {
                $scope.managers = response;
            });
        }
    ]).controller('contacts.DetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Contact.get({
                id: $state.params.id
            }, function(response) {
                $scope.contact = response;
            });
            $scope.deleteContact = function() {
                $scope.contact.$delete(function() {
                    notifier.success('The contact has been deleted');
                    $state.go('contacts.list');
                });
            };
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
            $scope.cancel = function() {
                $state.go('contacts.list');
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
                    $state.go('contacts.detail', {
                        id: $scope.contact.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('contacts.detail', {
                    id: $scope.contact.id
                });
            };
        }
    ]).controller('documents.ListCtrl', ['$scope', 'api', 'paginator',
        function($scope, api, paginator) {
            $scope.paginator = paginator();
            api.Document.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });

        }
    ]).controller('documents.DetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Document.get({
                id: $state.params.id
            }, function(response) {
                $scope.document = response;
            });

            $scope.deleteDocument = function() {
                $scope.document.$delete(function() {
                    notifier.success('Your document has been removed');
                    $state.go('documents.list');
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
            $scope.cancel = function() {
                $state.go('documents.list');
            };
        }
    ]).controller('parking.ListCtrl', ['$scope', 'api', 'paginator',
        function($scope, api, paginator) {
            $scope.paginator = paginator();
            api.Vehicle.query().$promise.then(function(response) {
                angular.forEach(response, function(item) {
                    item.searchTerms = item.description + " " + item.registration_number + item.resident.full_name;
                });
                $scope.paginator.reload(response);
            });

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
            $scope.cancel = function() {
                $state.go('parking.list');
            };
        }
    ]).controller('parking.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Vehicle.get({
                id: $state.params.id
            }, function(response) {
                $scope.vehicle = response;
            });

            $scope.deleteVehicle = function() {
                $scope.vehicle.$remove(function() {
                    notifier.success('Your vehicle has been removed');
                    $state.go('parking.list');
                });
            };

            $scope.save = function() {
                $scope.vehicle.$update(function() {
                    notifier.success('Your vehicle has been updated');
                    $state.go('parking.detail', {
                        id: $scope.vehicle.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('parking.detail', {
                    id: $scope.vehicle.id
                });
            };
        }
    ]).controller('parking.DetailCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            api.Vehicle.get({
                id: $state.params.id
            }, function(response) {
                $scope.vehicle = response;
            });
            $scope.deleteVehicle = function() {
                $scope.vehicle.$delete(function() {
                    notifier.success('Your vehicle has been removed');
                    $state.go('parking.list');
                });
            };
        }
    ]).controller('complaints.ListCtrl', ['$scope', 'api', 'paginator', 'auth',
        function($scope, api, paginator, auth) {
            $scope.cols = [
                'Complaint',
                'Date reported'
            ];
            if (auth.hasRole('manager')) {
                $scope.cols.push('Reported by');
            }
            $scope.paginator = paginator();
            api.Complaint.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
        }
    ]).controller('complaints.DetailCtrl', ['$scope', '$state', 'api',
        function($scope, $state, api) {
            api.Complaint.get({
                id: $state.params.id
            }, function(response) {
                $scope.complaint = response;
            });
        }
    ]).controller('complaints.NewCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {
            $scope.complaint = new api.Complaint();
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
            });

            $scope.save = function() {
                $scope.complaint.$save(function() {
                    notifier.success('Your complaint has been sent');
                    $state.go('complaints.list');
                });
            };
            $scope.cancel = function() {
                $state.go('complaints.list');
            };
        }
    ]).controller('tickets.ListCtrl', ['$scope', 'api', 'paginator',
        function($scope, api, paginator) {
            $scope.paginator = paginator();
            api.Ticket.query().$promise.then(function(response) {
                $scope.paginator.reload(response);
            });
        }
    ]).controller('tickets.NewCtrl', ['$scope', '$state', 'auth', 'api', 'notifier',
        function($scope, $state, auth, api, notifier) {
            $scope.ticket = new api.Ticket();
            if (auth.hasRole('manager')) {
                api.Apartment.query().$promise.then(function(response) {
                    $scope.apartments = response;
                });
            }
            $scope.save = function() {
                $scope.ticket.$save(function() {
                    notifier.success('Your issue has been saved');
                    $state.go('tickets.list');
                });
            };
            $scope.cancel = function() {
                $state.go('tickets.list');
            };
        }
    ]).controller('tickets.EditCtrl', ['$scope', '$state', 'api', 'notifier',
        function($scope, $state, api, notifier) {

            $scope.statusOptions = ["new", "accepted", "resolved"];

            api.Ticket.get({
                id: $state.params.id
            }, function(response) {
                $scope.ticket = response;
            });
            api.Apartment.query().$promise.then(function(response) {
                $scope.apartments = response;
            });
            $scope.save = function() {
                $scope.ticket.$update(function() {
                    notifier.success('Your issue has been saved');
                    $state.go('tickets.detail', {
                        id: $scope.ticket.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('tickets.detail', {
                    id: $scope.ticket.id
                });
            };
        }
    ]).controller('tickets.DetailCtrl', ['$scope', '$state', 'api',
        function($scope, $state, api) {
            api.Ticket.get({
                id: $state.params.id
            }, function(response) {
                $scope.ticket = response;
            });
        }
    ]).controller('account.EditCtrl', ['$scope', '$state', 'auth', 'api', 'notifier',
        function($scope, $state, auth, api, notifier) {
            $scope.save = function() {
                api.Auth.update(auth.user, function(response) {
                    auth.update(response);
                    notifier.success('Your account has been updated');
                    $state.go('residents.detail', {
                        id: auth.user.id
                    });
                }, function(response) {
                    $scope.serverErrors = response.data;
                });
            };
            $scope.cancel = function() {
                $state.go('residents.detail', {
                    id: auth.user.id
                });
            };
        }
    ]).controller('account.ChangePasswordCtrl', ['$scope', '$state', 'api', 'auth', 'notifier',
        function($scope, $state, api, auth, notifier) {
            function checkMatchingPassword() {
                if (($scope.user.password && $scope.user.password2) && $scope.user.password !== $scope.user.password2) {
                    $scope.passwordMismatch = true;
                } else {
                    $scope.passwordMismatch = false;
                }
            }

            $scope.user = {};
            $scope.passwordMismatch = false;
            $scope.$watch('user.password', function() {
                checkMatchingPassword();
            });
            $scope.$watch('user.password2', function() {
                checkMatchingPassword();
            });
            $scope.save = function() {
                api.Auth.changePassword($scope.user, function() {
                    notifier.success('Your password has been updated');
                    $state.go('residents.detail', {
                        id: auth.user.id
                    });
                });
            };
            $scope.cancel = function() {
                $state.go('residents.detail', {
                    id: auth.user.id
                });
            };

        }
    ]);
}());
