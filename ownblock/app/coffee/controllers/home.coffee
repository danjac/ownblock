angular.module("ownblock.controllers.home", [
  "ownblock"
  "ownblock.services"
]).controller("HomeCtrl", [
  "$scope"
  "api"
  ($scope, api) ->
    objects = {}
    $scope.timeline = []
    api.Timeline.get (response) ->
      getDateObj = (timestamp) ->
        timestamp = new Date(timestamp)
        date = new Date(timestamp.getFullYear(), timestamp.getMonth(), timestamp.getDate())
        obj = objects[date]
        unless angular.isDefined(obj)
          obj =
            date: date
            notices: []
            messages: []
            documents: []

          objects[date] = obj
        obj

      angular.forEach response.notices, (notice) ->
        dt = getDateObj(notice.created)
        dt.notices.push notice
        return

      angular.forEach response.messages, (msg) ->
        dt = getDateObj(msg.created)
        dt.messages.push msg

      angular.forEach response.documents, (doc) ->
        dt = getDateObj(doc.created)
        dt.documents.push doc

      angular.forEach objects, (obj) ->
        $scope.timeline.push obj

]
)
