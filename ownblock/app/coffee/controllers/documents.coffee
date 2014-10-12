angular.module("ownblock.controllers.documents", [
  "ui.router"
  "ui.calendar"
  "ui.bootstrap"
  "ownblock"
  "ownblock.services"
]).controller("documents.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.Document.query().$promise.then (response) ->
      $scope.paginator.reload response

]).controller("documents.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Document.get
      id: $state.params.id
    , (response) ->
      $scope.document = response

    $scope.deleteDocument = ->
      $scope.document.$delete ->
        notifier.success "Your document has been removed"
        $state.go "documents.list"

]).controller("documents.UploadCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.document = new api.Document()
    $scope.save = ->
      $scope.document.$save ->
        notifier.success "Your document has been uploaded"
        $state.go "documents.list"

    $scope.cancel = ->
      $state.go "documents.list"

])
