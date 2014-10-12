angular.module("ownblock.controllers.account", [
  "ownblock"
  "ownblock.services"
]).controller("account.EditCtrl", [
  "$scope"
  "$state"
  "auth"
  "api"
  "notifier"
  ($scope, $state, auth, api, notifier) ->
    $scope.save = ->
      api.Auth.update auth.user, ((response) ->
        auth.update response
        notifier.success "Your account has been updated"
        $state.go "residents.detail",
          id: auth.user.id

      ), (response) ->
        $scope.serverErrors = response.data


    $scope.cancel = ->
      $state.go "residents.detail",
        id: auth.user.id

]).controller("account.ChangePasswordCtrl", [
  "$scope"
  "$state"
  "api"
  "auth"
  "notifier"
  ($scope, $state, api, auth, notifier) ->
    checkMatchingPassword = ->
      if ($scope.user.password and $scope.user.password2) and $scope.user.password isnt $scope.user.password2
        $scope.passwordMismatch = true
      else
        $scope.passwordMismatch = false

    $scope.user = {}
    $scope.passwordMismatch = false
    $scope.$watch "user.password", ->
      checkMatchingPassword()

    $scope.$watch "user.password2", ->
      checkMatchingPassword()

    $scope.save = ->
      api.Auth.changePassword $scope.user, ->
        notifier.success "Your password has been updated"
        $state.go "residents.detail",
          id: auth.user.id

    $scope.cancel = ->
      $state.go "residents.detail",
        id: auth.user.id

])
