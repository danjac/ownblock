angular.module("ownblock.directives", [
  "ui.router"
  "ui.bootstrap"
  "ownblock"
  "ownblock.services"

]).directive("icon", ->
  restrict: "E"
  scope:
    name: "@"
    text: "@"

  template: "<i class=\"fa fa-{{name}}\"></i>&nbsp;{{text}}"

).directive("hasRole", [
  "auth"
  (auth) ->
    return (
      restrict: "A"
      link: (scope, element, attrs) ->
        element.remove()  unless auth.hasRole(attrs.hasRole)
    )

]).directive("paginatedTable", [
  "urls"
  (urls) ->
    return (
      restrict: "E"
      scope:
        paginator: "="
        cols: "="

      transclude: true
      replace: true
      templateUrl: urls.partials + "dataTable.html"
    )

]).directive("rowDef", ->
  restrict: "A"
  link: (scope, element, attrs, ctrl, transclude) ->
    transclude scope, (clone) ->
      angular.forEach clone, (item) ->
        if item.nodeName is "CELL"
          newElement = angular.element("<table><tr><td></td></tr></table>").find("td")
          newElement.append item
          newElement.attrs = item.attrs
          element.append newElement

).directive("searchForm", [
  "urls"
  (urls) ->
    SearchForm = ->
      @visible = false
      @filter = value: ""
      return

    SearchForm::toggle = ->
      @visible = not @visible
      @filter.value = ""  unless @visible
      return

    return (
      restrict: "E"
      scope:
        paginator: "="
        ifEmpty: "@"

      replace: true
      templateUrl: urls.partials + "searchForm.html"
      compile: ->
        pre: (scope, element, attrs) ->
          attrs.ifEmpty = attrs.ifEmpty or "Sorry, no results found for your search"

        post: (scope, element, attrs) ->
          form = new SearchForm()
          form.visible = true  if angular.isDefined(attrs.isVisible)
          scope.$parent[attrs.name] = scope[attrs.name] = form  if attrs.name
          scope.$watch attrs.name + ".filter.value", (newValue) ->
            filterObj = {}
            filterObj[attrs.filter] = newValue
            scope.paginator.filter filterObj  if scope.paginator
    )

]).directive("userLink", ->
  restrict: "E"
  scope:
    user: "="

  replace: true
  template: "<span><span ng-if=\"!user.is_active\">{{user.full_name}} <span class=\"label label-warning\">Removed</span></span><img ng-src=\"{{user.gravatar}}\" ng-if=\"user.gravatar\"> <a ng-if=\"user.is_active\" ui-sref=\"residents.detail({id: user.id})\">{{user.full_name}}</a></span>"
).directive("filesModel", ->
  controller: ($parse, $element, $attrs, $scope, $window) ->
    exp = $parse($attrs.filesModel)
    $element.on "change", ->
      exp.assign $scope, @files
      if $window.FileReader isnt null
        file = @files[0]
        reader = new $window.FileReader()
        reader.onload = ->
          $scope.upload = url: reader.result
          $scope.$apply()

        reader.readAsDataURL file
      $scope.$apply()

).directive("confirmDialog", [
  "$modal"
  "urls"
  ($modal, urls) ->
    modalInstanceCtrl = ($scope, $modalInstance, header, text) ->
      $scope.header = header
      $scope.text = text
      $scope.confirm = ->
        $modalInstance.close true

      $scope.cancel = ->
        $modalInstance.dismiss "cancel"

    openModal = (header, text, onConfirm) ->
      modalInstance = $modal.open(
        templateUrl: urls.partials + "confirmDialog.html"
        controller: modalInstanceCtrl
        resolve:
          header: ->
            header

          text: ->
            text
      )
      modalInstance.result.then (result) ->
        onConfirm()  if result


    return (
      restrict: "E"
      scope:
        onConfirm: "&"

      replace: true
      transclude: true
      template: "<button><div ng-transclude></div></button>"
      link: (scope, element, attrs) ->
        element.bind "click", (event) ->
          event.preventDefault()
          openModal attrs.header, attrs.text, scope.onConfirm
    )

]).directive "sendMessage", [
  "$modal"
  "auth"
  "api"
  "notifier"
  "urls"
  ($modal, auth, api, notifier, urls) ->
    modalInstanceCtrl = ($scope, $modalInstance, recipient, header) ->
      $scope.recipient = recipient
      $scope.message = new api.Message(
        recipient: recipient.id
        header: header or ""
      )
      $scope.send = ->
        $modalInstance.close $scope.message

      $scope.cancel = ->
        $modalInstance.dismiss "cancel"

    openModal = (recipient, header) ->
      modalInstance = $modal.open(
        templateUrl: urls.partials + "messages/modalForm.html"
        controller: modalInstanceCtrl
        resolve:
          recipient: ->
            recipient

          header: ->
            header
      )
      modalInstance.result.then (message) ->
        message.$save ->
          notifier.success "Your message has been sent"

    return (
      restrict: "E"
      scope:
        recipient: "=recipient"
        header: "@"

      replace: true
      transclude: true
      template: "<button role=\"button\"><div ng-transclude></div></button>"
      link: (scope, element, attrs) ->
        scope.$watch "recipient", (newVal) ->
          element.remove()  if newVal and newVal.id is auth.user.id

        element.bind "click", (event) ->
          event.preventDefault()
          openModal scope.recipient, scope.header

    )
]

