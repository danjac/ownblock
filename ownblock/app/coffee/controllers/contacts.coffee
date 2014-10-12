angular.module("ownblock.controllers.contacts", [
  "ownblock"
  "ownblock.services"
]).controller("contacts.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.Contact.query().$promise.then (response) ->
      $scope.paginator.reload response

    api.Resident.query(managers: true).$promise.then (response) ->
      $scope.managers = response

]).controller("contacts.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Contact.get
      id: $state.params.id
    , (response) ->
      $scope.contact = response

    $scope.deleteContact = ->
      $scope.contact.$delete ->
        notifier.success "The contact has been deleted"
        $state.go "contacts.list"

]).controller("contacts.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.contact = new api.Contact()
    $scope.save = ->
      $scope.contact.$save ->
        notifier.success "Your contact has been saved"
        $state.go "contacts.list"

    $scope.cancel = ->
      $state.go "contacts.list"
      return
]).controller("contacts.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Contact.get
      id: $state.params.id
    , (response) ->
      $scope.contact = response

    $scope.save = ->
      $scope.contact.$update ->
        notifier.success "Your contact has been saved"
        $state.go "contacts.detail",
          id: $scope.contact.id

    $scope.cancel = ->
      $state.go "contacts.detail",
        id: $scope.contact.id

])
