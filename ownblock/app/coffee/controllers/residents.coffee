angular.module("ownblock.controllers.residents", [
  "ownblock"
  "ownblock.services"
]).controller("residents.ListCtrl", [
  "$scope"
  "api"
  "auth"
  "paginator"
  ($scope, api, auth, paginator) ->
    $scope.user = auth.user
    $scope.paginator = paginator()
    api.Resident.query(residents: true).$promise.then (response) ->
      $scope.paginator.reload response

]).controller("residents.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.resident = new api.Resident()
    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.resident.$save (->
        notifier.success "The resident has been added"
        $state.go "residents.list"
      ), (response) ->
        $scope.serverErrors = response.data
      $scope.cancel = ->
        $state.go "residents.list"
]).controller("residents.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Resident.get
      id: $state.params.id
    , (response) ->
      $scope.resident = response

    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.resident.$update (->
        notifier.success "The resident has been updated"
        $state.go "residents.detail",
          id: $scope.resident.id

      ), (response) ->
        $scope.serverErrors = response.data
    $scope.cancel = ->
      $state.go "residents.detail",
        id: $scope.resident.id

]).controller("residents.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Resident.get
      id: $state.params.id
    , (response) ->
      $scope.resident = response

    $scope.deleteUser = ->
      $scope.resident.$delete ->
        notifier.success $scope.resident.full_name + " has been removed."
        $state.go "residents.list"

])
