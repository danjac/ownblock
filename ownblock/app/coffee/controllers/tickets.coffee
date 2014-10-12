angular.module("ownblock.controllers.tickets", [
  "ownblock"
  "ownblock.services"
]).controller("tickets.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.Ticket.query().$promise.then (response) ->
      $scope.paginator.reload response

]).controller("tickets.NewCtrl", [
  "$scope"
  "$state"
  "auth"
  "api"
  "notifier"
  ($scope, $state, auth, api, notifier) ->
    $scope.ticket = new api.Ticket()
    if auth.hasRole("manager")
      api.Apartment.query().$promise.then (response) ->
        $scope.apartments = response

    $scope.save = ->
      $scope.ticket.$save ->
        notifier.success "Your issue has been saved"
        $state.go "tickets.list"

    $scope.cancel = ->
      $state.go "tickets.list"

]).controller("tickets.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.statusOptions = [
      "new"
      "accepted"
      "resolved"
    ]
    api.Ticket.get
      id: $state.params.id
    , (response) ->
      $scope.ticket = response

    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.ticket.$update ->
        notifier.success "Your issue has been saved"
        $state.go "tickets.detail",
          id: $scope.ticket.id

      $scope.cancel = ->
        $state.go "tickets.detail",
          id: $scope.ticket.id

]).controller("tickets.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  ($scope, $state, api) ->
    api.Ticket.get
      id: $state.params.id
    , (response) ->
      $scope.ticket = response

])
