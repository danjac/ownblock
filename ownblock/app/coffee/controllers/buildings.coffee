angular.module("ownblock.controllers.buildings", [
  "ui.router"
  "ui.calendar"
  "ui.bootstrap"
  "ownblock"
  "ownblock.services"
]).controller("buildings.ListCtrl", [
  "$scope"
  "$state"
  "api"
  "auth"
  ($scope, $state, api, auth) ->
    getCity = (city) ->
      rv = null
      angular.forEach $scope.cities, (value) ->
        if value.name is city
          rv = value

      if rv is null
        rv =
          name: city
          buildings: []

        $scope.cities.push rv
      rv
    $scope.cities = []
    api.Building.query().$promise.then (response) ->
      angular.forEach response, (building) ->
        city = getCity(building.city)
        city.buildings.push building


    $scope.selectBuilding = (building) ->
      api.Building.get
        id: building.id
      , (response) ->
        auth.user.building = response
        $state.go "buildings.detail"

]).controller("buildings.DetailCtrl", [
  "$scope"
  "$state"
  "$window"
  "$modal"
  "api"
  "auth"
  "urls"
  ($scope, $state, $window, $modal, api, auth, urls) ->
    apartmentId = null
    showApartment = false
    if $state.params.id
      apartmentId = parseInt($state.params.id, 10)
      showApartment = true
    else apartmentId = auth.user.apartment  if auth.user.apartment
    $scope.apartmentSelector = id: apartmentId
    $scope.building = $scope.auth.user.building
    mapCreated = false
    $scope.generateMap = ->
      return  if mapCreated
      OL = $window.OpenLayers
      map = new OL.Map("map",
        controls: [
          new OL.Control.Navigation()
          new OL.Control.PanZoomBar()
          new OL.Control.ScaleLine()
          new OL.Control.MousePosition()
          new OL.Control.Permalink()
          new OL.Control.Attribution()
        ]
        maxExtent: new OL.Bounds(-180, -90, 180, 90)
        displayProjection: new OL.Projection("EPSG:4326")
        maxResolution: "auto"
      )
      fromProjection = new OL.Projection("EPSG:4326")
      toProjection = new OL.Projection("EPSG:900913")
      layer = new OL.Layer.OSM()
      point = new OL.LonLat($scope.building.longitude, $scope.building.latitude).transform(fromProjection, toProjection)
      markers = new OL.Layer.Markers("Markers")
      size = new OL.Size(21, 25)
      offset = new OL.Pixel(-(size.w / 2), -size.h)
      icon = new OL.Icon(urls.img + "marker.png", size, offset)
      map.addLayer layer
      map.addLayer markers
      map.setCenter point, 16
      markers.addMarker new OL.Marker(point, icon)
      mapCreated = true

    $scope.apartments = []
    $scope.tabs =
      building:
        active: true

      apartments:
        active: false

    $scope.tabs.apartments.active = true  if showApartment
    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.selectApartment = ->
      unless $scope.apartmentSelector.id
        $scope.currentApartment = null

      api.Apartment.get
        id: $scope.apartmentSelector.id
      , (response) ->
        $scope.currentApartment = response

    $scope.selectApartment()
    $scope.addResident = (apartment) ->
      modalInstanceCtrl = ($scope, $modalInstance) ->
        $scope.resident = {}
        $scope.cancel = ->
          $modalInstance.dismiss "cancel"

        $scope.save = ->
          $modalInstance.close $scope.resident

      modalInstance = $modal.open(
        templateUrl: urls.partials + "buildings/modalResidentForm.html"
        controller: modalInstanceCtrl
      )
      modalInstance.result.then (resident) ->
        api.Apartment.addResident(
          id: apartment.id
        , resident).$promise.then (response) ->
          $scope.currentApartment.users.push response

]
)
