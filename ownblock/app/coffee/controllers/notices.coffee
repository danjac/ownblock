angular.module("ownblock.controllers.notices", [
  "ownblock"
  "ownblock.services"
]).controller("notices.NewCtrl", [
  "$scope"
  "$state"
  "notifier"
  "api"
  ($scope, $state, notifier, api) ->
    $scope.notice = new api.Notice()
    $scope.save = ->
      $scope.notice.$save ->
        notifier.success "Your notice has been published"
        $state.go "notices.list"

      $scope.cancel = ->
        $state.go "notices.list"
]).controller("notices.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  "urls"
  ($scope, api, paginator, urls) ->
    $scope.paginator = paginator()
    api.Notice.query().$promise.then (response) ->
      angular.forEach response, (item) ->
        item.searchTerms = item.title + " " + item.details + item.author.full_name

      $scope.paginator.reload response

]).controller("notices.DetailCtrl", [
  "$scope"
  "$state"
  "notifier"
  "api"
  ($scope, $state, notifier, api) ->
    api.Notice.get
      id: $state.params.id
    , (response) ->
      $scope.notice = response

    $scope.deleteNotice = ->
      $scope.notice.$delete ->
        notifier.success "Your notice has been removed"
        $state.go "notices.list"

]).controller("notices.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Notice.get
      id: $state.params.id
    , (response) ->
      $scope.notice = response

    $scope.save = ->
      $scope.notice.$update ->
        notifier.success "Your notice has been updated"
        $state.go "notices.detail",
          id: $scope.notice.id

    $scope.cancel = ->
      $state.go "notices.detail",
        id: $scope.notice.id

])
