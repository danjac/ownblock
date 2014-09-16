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
        urls: {
            static: '/static/',
            partials: '/static/partials/',
            img: '/static/img/'
        }
    }).
    config(['$httpProvider',
        '$resourceProvider',
        '$stateProvider',
        '$urlRouterProvider',
        'urls',
        function(
            $httpProvider,
            $resourceProvider,
            $stateProvider,
            $urlRouterProvider,
            urls) {

            $resourceProvider.defaults.stripTrailingSlashes = true;

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

            $httpProvider.interceptors.push(function($q, $location, notifier) {
                return {
                    'responseError': function(response) {
                        console.log(response);
                        var warning = "Sorry, an error has occurred",
                            result = $q.reject(response);
                        switch (response.status) {
                            case 401:
                            case 403:
                                // we're out of sync with server, logout 
                                $location.path("accessdenied");
                                return result;
                            case 404:
                                $location.path("notfound");
                                return result;
                            case 400:
                                warning = "Sorry, your form appears to have some errors";
                                break;
                            case 413:
                                warning = "Sorry, your upload was too large";
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
                templateUrl: urls.partials + 'base.html',
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
                templateUrl: urls.partials + 'accessDenied.html',
            }).
            state('notfound', {
                url: '/notfound',
                templateUrl: urls.partials + 'notfound.html',
            }).
            state('account', {
                templateUrl: urls.partials + 'account/base.html',
                parent: 'site'
            }).
            state('account.edit', {
                url: '/account',
                templateUrl: urls.partials + 'account/edit.html',
                controller: 'account.EditCtrl'
            }).
            state('account.password', {
                url: '/account/pass',
                templateUrl: urls.partials + 'account/passwordForm.html',
                controller: 'account.ChangePasswordCtrl'
            }).
            state('residents', {
                templateUrl: urls.partials + 'residents/base.html',
                parent: 'site'
            }).
            state('residents.list', {
                url: '/residents',
                templateUrl: urls.partials + 'residents/list.html',
                controller: 'residents.ListCtrl'
            }).
            state('residents.new', {
                url: '/residents/new',
                templateUrl: urls.partials + 'residents/form.html',
                controller: 'residents.NewCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('residents.edit', {
                url: '/residents/:id/edit',
                templateUrl: urls.partials + 'residents/form.html',
                controller: 'residents.EditCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('residents.detail', {
                url: '/residents/:id',
                templateUrl: urls.partials + 'residents/detail.html',
                controller: 'residents.DetailCtrl'
            }).
            state('messages', {
                templateUrl: urls.partials + 'messages/base.html',
                parent: 'site'
            }).
            state('messages.list', {
                url: '/messages',
                templateUrl: urls.partials + 'messages/list.html',
                controller: 'messages.ListCtrl',
            }).
            state('messages.detail', {
                url: '/messages/:id',
                templateUrl: urls.partials + 'messages/detail.html',
                controller: 'messages.DetailCtrl',
            }).
            state('messages.send', {
                url: '/messages/send/:recipient',
                templateUrl: urls.partials + 'messages/form.html',
                controller: 'messages.SendCtrl'
            }).
            state('messages.reply', {
                url: '/messages/reply/:parent',
                templateUrl: urls.partials + 'messages/form.html',
                controller: 'messages.ReplyCtrl'
            }).
            state('notices', {
                templateUrl: urls.partials + 'notices/base.html',
                parent: 'site'
            }).
            state('notices.list', {
                url: '/notices',
                templateUrl: urls.partials + 'notices/list.html',
                controller: 'notices.ListCtrl'
            }).
            state('notices.new', {
                url: '/notices/new',
                templateUrl: urls.partials + 'notices/form.html',
                controller: 'notices.NewCtrl'
            }).
            state('notices.detail', {
                url: '/notices/:id',
                templateUrl: urls.partials + 'notices/detail.html',
                controller: 'notices.DetailCtrl'
            }).
            state('notices.edit', {
                url: '/notices/:id/edit',
                templateUrl: urls.partials + 'notices/form.html',
                controller: 'notices.EditCtrl'
            }).
            state('amenities', {
                templateUrl: urls.partials + 'amenities/base.html',
                parent: 'site'
            }).
            state('amenities.list', {
                url: '/amenities',
                templateUrl: urls.partials + 'amenities/list.html',
                controller: 'amenities.ListCtrl'
            }).
            state('amenities.newAmenity', {
                url: '/amenities/new',
                templateUrl: urls.partials + 'amenities/amenityForm.html',
                controller: 'amenities.NewAmenityCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('amenities.edit', {
                url: '/amenities/:id/edit',
                templateUrl: urls.partials + 'amenities/amenityForm.html',
                controller: 'amenities.EditAmenityCtrl'
            }).
            state('amenities.detail', {
                url: '/amenities/:id',
                templateUrl: urls.partials + 'amenities/detail.html',
                controller: 'amenities.DetailCtrl'
            }).
            state('amenities.newTicket', {
                url: '/amenities/:id/ticket',
                templateUrl: urls.partials + 'amenities/ticketForm.html',
                controller: 'amenities.NewTicketCtrl'
            }).
            state('amenities.bookingDetail', {
                url: '/amenities/bookings/:id',
                templateUrl: urls.partials + 'amenities/bookingDetail.html',
                controller: 'amenities.BookingDetailCtrl'
            }).
            state('amenities.editBooking', {
                url: '/amenities/bookings/:id/edit',
                templateUrl: urls.partials + 'amenities/bookingForm.html',
                controller: 'amenities.EditBookingCtrl'
            }).
            state('amenities.newBooking', {
                url: '/amenities/:id/bookings/new',
                templateUrl: urls.partials + 'amenities/bookingForm.html',
                controller: 'amenities.NewBookingCtrl',
                data: {
                    access: 'resident'
                }
            }).
            state('complaints', {
                templateUrl: urls.partials + 'complaints/base.html',
                parent: 'site'
            }).
            state('complaints.list', {
                url: '/complaints',
                templateUrl: urls.partials + 'complaints/list.html',
                controller: 'complaints.ListCtrl'
            }).
            state('complaints.new', {
                url: '/complaints/new',
                templateUrl: urls.partials + 'complaints/form.html',
                controller: 'complaints.NewCtrl',
                data: {
                    access: 'resident'
                }
            }).
            state('complaints.detail', {
                url: '/complaints/:id',
                templateUrl: urls.partials + 'complaints/detail.html',
                controller: 'complaints.DetailCtrl'
            }).
            state('tickets', {
                templateUrl: urls.partials + 'tickets/base.html',
                parent: 'site'
            }).
            state('tickets.list', {
                url: '/tickets',
                templateUrl: urls.partials + 'tickets/list.html',
                controller: 'tickets.ListCtrl'
            }).
            state('tickets.new', {
                url: '/tickets/new',
                templateUrl: urls.partials + 'tickets/form.html',
                controller: 'tickets.NewCtrl'
            }).
            state('tickets.detail', {
                url: '/tickets/:id',
                templateUrl: urls.partials + 'tickets/detail.html',
                controller: 'tickets.DetailCtrl'
            }).
            state('tickets.edit', {
                url: '/tickets/:id/edit',
                templateUrl: urls.partials + 'tickets/form.html',
                controller: 'tickets.EditCtrl'
            }).
            state('storage', {
                templateUrl: urls.partials + 'storage/base.html',
                parent: 'site'
            }).
            state('storage.list', {
                url: '/storage',
                templateUrl: urls.partials + 'storage/list.html',
                controller: 'storage.ListCtrl'
            }).
            state('storage.newItem', {
                url: '/storage/items/new',
                templateUrl: urls.partials + 'storage/itemForm.html',
                controller: 'storage.NewItemCtrl',
                data: {
                    access: 'resident'
                }
            }).
            state('storage.newPlace', {
                url: '/storage/places/new',
                templateUrl: urls.partials + 'storage/placeForm.html',
                controller: 'storage.NewPlaceCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('storage.itemDetail', {
                url: '/storage/:id',
                templateUrl: urls.partials + 'storage/itemDetail.html',
                controller: 'storage.ItemDetailCtrl'
            }).
            state('storage.placeDetail', {
                url: '/storage/places/:id',
                templateUrl: urls.partials + 'storage/placeDetail.html',
                controller: 'storage.PlaceDetailCtrl'
            }).
            state('storage.editItem', {
                url: '/storage/:id/edit',
                templateUrl: urls.partials + 'storage/itemForm.html',
                controller: 'storage.EditItemCtrl'
            }).
            state('storage.editPlace', {
                url: '/storage/places/:id/edit',
                templateUrl: urls.partials + 'storage/placeForm.html',
                controller: 'storage.EditPlaceCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('documents', {
                templateUrl: urls.partials + 'documents/base.html',
                parent: 'site'
            }).
            state('documents.list', {
                url: '/docs',
                templateUrl: urls.partials + 'documents/list.html',
                controller: 'documents.ListCtrl'
            }).
            state('documents.upload', {
                url: '/docs/upload',
                templateUrl: urls.partials + 'documents/form.html',
                controller: 'documents.UploadCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('documents.detail', {
                url: '/docs/:id',
                templateUrl: urls.partials + 'documents/detail.html',
                controller: 'documents.DetailCtrl'
            }).
            state('parking', {
                templateUrl: urls.partials + 'parking/base.html',
                parent: 'site'
            }).
            state('parking.list', {
                url: '/parking',
                templateUrl: urls.partials + 'parking/list.html',
                controller: 'parking.ListCtrl'
            }).
            state('parking.new', {
                url: '/parking/new',
                templateUrl: urls.partials + 'parking/vehicleForm.html',
                controller: 'parking.NewCtrl'
            }).
            state('parking.detail', {
                url: '/parking/:id',
                templateUrl: urls.partials + 'parking/detail.html',
                controller: 'parking.DetailCtrl'
            }).
            state('parking.edit', {
                url: '/parking/:id/edit',
                templateUrl: urls.partials + 'parking/vehicleForm.html',
                controller: 'parking.EditCtrl'
            }).
            state('contacts', {
                templateUrl: urls.partials + 'contacts/base.html',
                parent: 'site'
            }).
            state('contacts.list', {
                url: '/contacts',
                templateUrl: urls.partials + 'contacts/list.html',
                controller: 'contacts.ListCtrl'
            }).
            state('contacts.new', {
                url: '/contacts/new',
                templateUrl: urls.partials + 'contacts/form.html',
                controller: 'contacts.NewCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('contacts.detail', {
                url: '/contacts/:id',
                templateUrl: urls.partials + 'contacts/detail.html',
                controller: 'contacts.DetailCtrl'
            }).
            state('contacts.edit', {
                url: '/contacts/:id/edit',
                templateUrl: urls.partials + 'contacts/form.html',
                controller: 'contacts.EditCtrl',
                data: {
                    access: 'manager'
                }
            }).
            state('buildings', {
                templateUrl: urls.partials + 'buildings/base.html',
                parent: 'site'
            }).
            state('buildings.list', {
                url: '/building/list',
                templateUrl: urls.partials + 'buildings/list.html',
                controller: 'buildings.ListCtrl',
                data: {
                    acess: 'manager'
                }
            }).
            state('buildings.apartment', {
                url: '/building/:id',
                templateUrl: urls.partials + 'buildings/detail.html',
                controller: 'buildings.DetailCtrl'
            }).
            state('buildings.detail', {
                url: '/building',
                templateUrl: urls.partials + 'buildings/detail.html',
                controller: 'buildings.DetailCtrl'
            });

            $urlRouterProvider.otherwise('/building');

        }
    ]).run(['$rootScope', '$state', 'auth',
        function($rootScope, $state, auth) {

            // fetch the current user from the session. If the user is not logged in,
            // redirect to the external login page; otherwise sync user details with the 
            // application.
            $rootScope.$on('$stateChangeStart', function(event, toState) {
                if (!auth.authorize(toState)) {
                    event.preventDefault();
                    $state.transitionTo('accessdenied');
                }

            });
        }
    ]);
}());

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

(function() {
    'use strict';
    angular.module('ownblock.directives', [
        'ui.router',
        'ui.bootstrap',
        'ownblock',
        'ownblock.services'
    ]).
    directive('icon', function() {
        return {
            restrict: 'E',
            scope: {
                name: '@',
                text: '@'
            },
            template: '<i class="fa fa-{{name}}"></i>&nbsp;{{text}}'
            //template: '<span class="glyphicon glyphicon-{{name}}"></span>&nbsp;{{text}}'
        };
    }).
    directive('hasRole', ['auth',
        function(auth) {
            return {
                restrict: 'A',
                link: function(scope, element, attrs) {
                    if (!auth.hasRole(attrs.hasRole)) {
                        element.remove();
                    }
                }

            };
        }
    ]).
    directive('paginatedTable', ['urls',
        function(urls) {
            return {
                restrict: 'E',
                scope: {
                    paginator: '=',
                    cols: '='
                },
                transclude: true,
                replace: true,
                templateUrl: urls.partials + 'dataTable.html'
            };
        }
    ]).
    directive('rowDef', function() {
        return {
            restrict: 'A',
            link: function(scope, element, attrs, ctrl, transclude) {

                transclude(scope, function(clone) {
                    angular.forEach(clone, function(item) {
                        if (item.nodeName === 'CELL') {
                            // hack around this bug: https://github.com/angular/angular.js/issues/1459
                            var newElement = angular.element('<table><tr><td></td></tr></table>').find('td');
                            newElement.append(item);
                            element.append(newElement);
                        }
                    });
                });
            }
        };
    }).
    directive('searchForm', ['urls',
        function(urls) {
            var SearchForm = function() {
                this.visible = false;
                this.filter = {
                    value: ''
                };
            };
            SearchForm.prototype.toggle = function() {
                this.visible = !this.visible;
                if (!this.visible) {
                    this.filter.value = '';
                }
            };
            return {
                restrict: 'E',
                scope: {
                    paginator: '=',
                    ifEmpty: '@'
                },
                replace: true,
                templateUrl: urls.partials + 'searchForm.html',
                compile: function() {
                    return {
                        pre: function(scope, element, attrs) {
                            attrs.ifEmpty = attrs.ifEmpty || 'Sorry, no results found for your search';
                        },
                        post: function(scope, element, attrs) {
                            var form = new SearchForm();
                            if (angular.isDefined(attrs.isVisible)) {
                                form.visible = true;
                            }
                            if (attrs.name) {
                                scope.$parent[attrs.name] = scope[attrs.name] = form;
                            }
                            scope.$watch(attrs.name + '.filter.value', function(newValue) {
                                var filterObj = {};
                                filterObj[attrs.filter] = newValue;
                                if (scope.paginator) {
                                    scope.paginator.filter(filterObj);
                                }
                            });

                        }
                    };
                }
            };
        }
    ]).
    directive('userLink', function() {
        return {
            restrict: 'E',
            scope: {
                user: '='
            },
            replace: true,
            template: '<span><span ng-if="!user.is_active">{{user.full_name}} <span class="label label-warning">Removed</span></span><img ng-src="{{user.gravatar}}" ng-if="user.gravatar"> <a ng-if="user.is_active" ui-sref="residents.detail({id: user.id})">{{user.full_name}}</a></span>'
        };
    }).
    directive('filesModel', function() {
        /* https://github.com/angular/angular.js/issues/1375#issuecomment-21933012 */
        return {
            controller: function($parse, $element, $attrs, $scope, $window) {
                var exp = $parse($attrs.filesModel);
                $element.on('change', function() {
                    exp.assign($scope, this.files);
                    if ($window.FileReader !== null) {
                        var file = this.files[0],
                            reader = new $window.FileReader();
                        reader.onload = function() {
                            $scope.upload = {
                                url: reader.result
                            };
                            $scope.$apply();
                        };
                        reader.readAsDataURL(file);
                    }

                    $scope.$apply();
                });
            }
        };
    }).
    directive('confirmDialog', ['$modal', 'urls',
        function($modal, urls) {
            var modalInstanceCtrl = function($scope, $modalInstance, header, text) {
                    $scope.header = header;
                    $scope.text = text;
                    $scope.confirm = function() {
                        $modalInstance.close(true);
                    };
                    $scope.cancel = function() {
                        $modalInstance.dismiss('cancel');
                    };
                },
                openModal = function(header, text, onConfirm) {
                    var modalInstance = $modal.open({
                        templateUrl: urls.partials + 'confirmDialog.html',
                        controller: modalInstanceCtrl,
                        resolve: {
                            header: function() {
                                return header;
                            },
                            text: function() {
                                return text;
                            }
                        }
                    });
                    modalInstance.result.then(function(result) {
                        if (result) {
                            onConfirm();
                        }
                    });
                };
            return {
                restrict: 'E',
                scope: {
                    onConfirm: '&'
                },
                replace: true,
                transclude: true,
                template: '<button><div ng-transclude></div></button>',
                link: function(scope, element, attrs) {
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(attrs.header, attrs.text, scope.onConfirm);
                    });
                }
            };

        }
    ]).directive('sendMessage', ['$modal', 'auth', 'api', 'notifier', 'urls',
        function($modal, auth, api, notifier, urls) {
            var modalInstanceCtrl = function($scope, $modalInstance, recipient, header) {

                    $scope.recipient = recipient;
                    $scope.message = new api.Message({
                        recipient: recipient.id,
                        header: header || ''
                    });
                    $scope.send = function() {
                        $modalInstance.close($scope.message);
                    };
                    $scope.cancel = function() {
                        $modalInstance.dismiss('cancel');
                    };
                },
                openModal = function(recipient, header) {
                    var modalInstance = $modal.open({
                        templateUrl: urls.partials + 'messages/modalForm.html',
                        controller: modalInstanceCtrl,
                        resolve: {
                            recipient: function() {
                                return recipient;
                            },
                            header: function() {
                                return header;
                            }
                        }
                    });
                    modalInstance.result.then(function(message) {
                        message.$save(function() {
                            notifier.success('Your message has been sent');
                        });
                    });

                };
            return {
                restrict: 'E',
                scope: {
                    recipient: '=recipient',
                    header: '@'
                },
                replace: true,
                transclude: true,
                template: '<button role="button"><div ng-transclude></div></button>',
                link: function(scope, element, attrs) {
                    scope.$watch('recipient', function(newVal) {
                        if (newVal && newVal.id === auth.user.id) {
                            //attrs.$set('ngDisabled', true);
                            //element.addClass('disabled');
                            element.remove();
                        }
                    });
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(scope.recipient, scope.header);
                    });
                }
            };
        }
    ]);
}());

(function() {
    'use strict';
    angular.module('ownblock.services', [
        'ngResource'
    ]).
    service('auth', [

        function() {

            return {
                authorize: function(state) {
                    var data = state.data || {},
                        access = data.access || null;

                    return this.hasRole(access);
                },
                hasRole: function(access) {
                    if (!access) {
                        return true;
                    }
                    return (this.user && this.user.role === access);
                },
                sync: function(response) {
                    this.user = response;
                },
                update: function(response) {
                    this.user.first_name = response.first_name;
                    this.user.last_name = response.last_name;
                    this.user.email = response.email;
                    this.user.full_name = response.full_name;
                }
            };
        }
    ]).factory('notifier', ['$rootScope',
        function($rootScope) {
            var Notifier = function() {
                this.notifications = [];
            };
            Notifier.prototype.notify = function(type, msg) {
                var notification = {
                    type: type,
                    message: msg
                };
                $rootScope.$broadcast('Notifier.new', notification);
                this.notifications.push(notification);
            };
            Notifier.prototype.dismiss = function(index) {
                this.notifications.splice(index, 1);
            };
            Notifier.prototype.remove = function(notification) {
                var index = this.notifications.indexOf(notification);
                this.dismiss(index);
            };
            Notifier.prototype.success = function(msg) {
                this.notify('success', msg);
            };
            Notifier.prototype.warning = function(msg) {
                this.notify('warning', msg);
            };
            Notifier.prototype.info = function(msg) {
                this.notify('info', msg);
            };
            Notifier.prototype.danger = function(msg) {
                this.notify('danger', msg);
            };
            return new Notifier();
        }
    ]).factory('paginator', ['$filter',
        function($filter) {

            var Paginator = function(items, maxSize) {
                this.maxSize = maxSize || 10;
                this.reload(items);
            };

            Paginator.prototype.change = function() {
                var offset = (this.page - 1) * this.maxSize;
                this.currentItems = this.filteredItems.slice(offset, offset + this.maxSize);
                this.isEmpty = this.currentItems.length === 0;
            };

            Paginator.prototype.reload = function(items) {
                this.items = this.filteredItems = items || [];
                this.total = this.items.length;
                this.page = 1;
                this.change();
            };

            Paginator.prototype.filter = function(value) {
                if (value) {
                    this.filteredItems = $filter('filter')(this.items, value);
                } else {
                    this.filteredItems = this.items;
                }
                this.total = this.filteredItems.length;
                this.change();
            };

            Paginator.prototype.remove = function(index) {
                this.items.splice(index, 1);
                this.items.total = this.items.length;
                this.change();
            };

            return function(items, maxSize) {
                return new Paginator(items, maxSize);
            };

        }
    ]).service('api', ['$resource',
        function($resource) {

            function makeEndpoint(url, actions) {
                if (!angular.isDefined(actions)) {
                    actions = {
                        update: {
                            method: 'PUT'
                        }
                    };
                }
                return $resource(url, {
                    id: '@id',
                }, actions);
            }

            return {
                Notice: makeEndpoint('/api/notices/notices/:id'),
                Message: makeEndpoint('/api/messages/messages/:id'),
                Resident: makeEndpoint('/api/users/people/:id'),
                Amenity: makeEndpoint('/api/amenities/items/:id'),
                Booking: makeEndpoint('/api/amenities/bookings/:id'),
                Place: makeEndpoint('/api/storage/places/:id'),
                Document: makeEndpoint('/api/documents/documents/:id'),
                Contact: makeEndpoint('/api/contacts/contacts/:id'),
                Vehicle: makeEndpoint('/api/parking/vehicles/:id'),
                Complaint: makeEndpoint('/api/complaints/complaints/:id'),
                Ticket: makeEndpoint('/api/tickets/tickets/:id'),
                StorageItem: makeEndpoint('/api/storage/items/:id', {
                    removePhoto: {
                        url: '/api/storage/items/:id/remove_photo',
                        method: 'PATCH'
                    },
                    update: {
                        method: 'PUT'
                    }
                }),
                Apartment: makeEndpoint('/api/buildings/apartments/:id', {
                    addResident: {
                        url: '/api/buildings/apartments/:id/add_resident',
                        method: 'POST'
                    }
                }),
                Building: makeEndpoint('/api/buildings/buildings/:id'),
                Timeline: $resource('/api/buildings/timeline'),
                Auth: $resource('/api/users/auth/', {}, {
                    update: {
                        method: 'PUT'
                    },
                    changePassword: {
                        method: 'PATCH'
                    }
                })
            };
        }
    ]);
}());
