angular.module("ownblock.controllers.app", [
  "ownblock"
  "ownblock.services"
]).controller("AppCtrl", [
  "$scope"
  "$location"
  "$state"
  "$timeout"
  "auth"
  "notifier"
  "urls"
  ($scope, $location, $state, $timeout, auth, notifier, urls) ->
    $scope.auth = auth
    $scope.notifier = notifier
    $scope.includes = (name) ->
      $state.includes name

    $scope.init = (user) ->
      $location.path "/account/login/"  unless user
      auth.sync user

    $scope.$on "Notifier.new", (event, notification) ->
      $timeout (->
        notifier.remove notification
      ), 3000

    $scope.menuTpl = urls.partials + "menu.html"
])


