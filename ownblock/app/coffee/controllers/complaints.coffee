angular.module("ownblock.controllers.complaints", [
  "ownblock"
  "ownblock.services"
]).controller("complaints.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  "auth"
  ($scope, api, paginator, auth) ->
    $scope.cols = [
      "Complaint"
      "Date reported"
    ]
    $scope.cols.push "Reported by"  if auth.hasRole("manager")
    $scope.paginator = paginator()
    api.Complaint.query().$promise.then (response) ->
      $scope.paginator.reload response

]).controller("complaints.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  ($scope, $state, api) ->
    api.Complaint.get
      id: $state.params.id
    , (response) ->
      $scope.complaint = response

]).controller("complaints.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.complaint = new api.Complaint()
    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.complaint.$save ->
        notifier.success "Your complaint has been sent"
        $state.go "complaints.list"

    $scope.cancel = ->
      $state.go "complaints.list"

])
