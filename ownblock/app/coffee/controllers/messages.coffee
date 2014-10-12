angular.module("ownblock.controllers.messages", [
  "ownblock"
  "ownblock.services"
]).controller("messages.ListCtrl", [
  "$scope"
  "api"
  "auth"
  "paginator"
  ($scope, api, auth, paginator) ->
    api.Message.query().$promise.then (response) ->
      received = []
      sent = []
      angular.forEach response, (message) ->
        message.searchTerms = message.header + " " + message.received
        if message.recipient is auth.user.id
          message.searchTerms += " " + message.sender.full_name
          received.push message
        else
          message.searchTerms += " " + message.recipient_detail.full_name
          sent.push message

      $scope.receivedMessages = paginator(received)
      $scope.sentMessages = paginator(sent)

]).controller("messages.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  ($scope, $state, api) ->
    api.Message.get
      id: $state.params.id
    , (response) ->
      $scope.message = response

]).controller("messages.SendCtrl", [
  "$scope"
  "$state"
  "$stateParams"
  "api"
  "notifier"
  ($scope, $state, $stateParams, api, notifier) ->
    $scope.message = new api.Message(recipient: $stateParams.recipient)
    $scope.send = ->
      $scope.message.$save (->
        notifier.success "Your message has been sent"
        $state.go "messages.list"
      ), (response) ->


        $scope.cancel = ->
          $state.go "messages.list"
]).controller("messages.ReplyCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.message = new api.Message(parent: $state.params.parent)
    api.Message.get(id: $state.params.parent).$promise.then (response) ->
      $scope.message.header = "Re: " + response.header
      $scope.message.details = "> " + response.details  if response.details
      $scope.message.recipient = response.sender.id

    $scope.send = ->
      $scope.message.$save ->
        notifier.success "Your message has been sent"
        $state.go "messages.list"


    $scope.cancel = ->
      $state.go "messages.detail",
        id: $state.params.parent

])
