angular.module("ownblock.controllers.parking", [
  "ownblock"
  "ownblock.services"
]).controller("parking.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.Vehicle.query().$promise.then (response) ->
      angular.forEach response, (item) ->
        item.searchTerms = item.description + " " + item.registration_number + item.resident.full_name

      $scope.paginator.reload response

]).controller("parking.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.vehicle = new api.Vehicle()
    $scope.save = ->
      $scope.vehicle.$save ->
        notifier.success "Your vehicle has been added"
        $state.go "parking.list"

    $scope.cancel = ->
      $state.go "parking.list"

]).controller("parking.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Vehicle.get
      id: $state.params.id
    , (response) ->
      $scope.vehicle = response

    $scope.deleteVehicle = ->
      $scope.vehicle.$remove ->
        notifier.success "Your vehicle has been removed"
        $state.go "parking.list"

    $scope.save = ->
      $scope.vehicle.$update ->
        notifier.success "Your vehicle has been updated"
        $state.go "parking.detail",
          id: $scope.vehicle.id

    $scope.cancel = ->
      $state.go "parking.detail",
        id: $scope.vehicle.id

]).controller("parking.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Vehicle.get
      id: $state.params.id
    , (response) ->
      $scope.vehicle = response

    $scope.deleteVehicle = ->
      $scope.vehicle.$delete ->
        notifier.success "Your vehicle has been removed"
        $state.go "parking.list"

])
