angular.module("ownblock.controllers.storage", [
  "ownblock"
  "ownblock.services"
]).controller("storage.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.StorageItem.query().$promise.then (response) ->
      $scope.paginator.reload response

    api.Place.query().$promise.then (response) ->
      $scope.places = response

]).controller("storage.NewPlaceCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.place = new api.Place()
    $scope.save = ->
      $scope.place.$save ->
        notifier.success "The storage area has been added"
        $state.go "storage.list"

]).controller("storage.NewItemCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.item = new api.StorageItem()
    $scope.places = []
    $scope.editPhoto = true
    $scope.showPhoto = false
    api.Place.query().$promise.then (response) ->
      $scope.places = response

    $scope.save = ->
      $scope.item.$save ->
        notifier.success "Your item has been added"
        $state.go "storage.list"

    $scope.cancel = ->
      $state.go "storage.list"
      return
]).controller("storage.EditItemCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.editPhoto = false
    $scope.showPhoto = false
    $scope.places = []
    api.StorageItem.get
      id: $state.params.id
    , (response) ->
      $scope.item = response
      $scope.showPhoto = $scope.item.photo
      $scope.editPhoto = not $scope.showPhoto

    $scope.toggleEditPhoto = ->
      $scope.editPhoto = not $scope.editPhoto

    $scope.deletePhoto = ->
      $scope.item.$removePhoto ->
        $scope.item.photo = null
        $scope.showPhoto = false
        $scope.editPhoto = true
        notifier.success "Your photo has been removed"

    api.Place.query().$promise.then (response) ->
      $scope.places = response

    $scope.save = ->
      $scope.item.$update ->
        notifier.success "Your item has been updated"
        $state.go "storage.itemDetail",
          id: $scope.item.id


    $scope.cancel = ->
      $state.go "storage.itemDetail",
        id: $scope.item.id

]).controller("storage.ItemDetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.StorageItem.get
      id: $state.params.id
    , (response) ->
      $scope.item = response

    $scope.deleteItem = ->
      $scope.item.$delete ->
        notifier.success "Your item has been removed"
        $state.go "storage.list"
]).controller("storage.PlaceDetailCtrl", [
  "$scope"
  "$state"
  "api"
  "paginator"
  "notifier"
  ($scope, $state, api, paginator, notifier) ->
    $scope.paginator = paginator()
    api.Place.get
      id: $state.params.id
    , (response) ->
      $scope.place = response
      $scope.paginator.reload $scope.place.items

    $scope.deletePlace = ->
      $scope.place.$delete ->
        notifier.success "Storage area has been removed"
        $state.go "storage.list"

]).controller("storage.EditPlaceCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Place.get
      id: $state.params.id
    , (response) ->
      $scope.place = response

    $scope.save = ->
      $scope.place.$update ->
        notifier.success "The storage area has been updated"
        $state.go "storage.placeDetail",
          id: $scope.place.id


    $scope.cancel = ->
      $state.go "storage.placeDetail",
        id: $scope.place.id

])
