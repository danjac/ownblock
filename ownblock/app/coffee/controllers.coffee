angular.module("ownblock.controllers", [
  "ui.router"
  "ui.calendar"
  "ui.bootstrap"
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

]).controller("storage.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.StorageItem.query().$promise.then (response) ->
      $scope.paginator.reload response

    api.Place.query().$promise.then (response) ->
      $scope.places = response

]).controller("storage.NewPlaceCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.place = new api.Place()
    $scope.save = ->
      $scope.place.$save ->
        notifier.success "The storage area has been added"
        $state.go "storage.list"

]).controller("storage.NewItemCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.item = new api.StorageItem()
    $scope.places = []
    $scope.editPhoto = true
    $scope.showPhoto = false
    api.Place.query().$promise.then (response) ->
      $scope.places = response

    $scope.save = ->
      $scope.item.$save ->
        notifier.success "Your item has been added"
        $state.go "storage.list"

    $scope.cancel = ->
      $state.go "storage.list"
      return
    ]).controller("storage.EditItemCtrl", [
      "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.editPhoto = false
    $scope.showPhoto = false
    $scope.places = []
    api.StorageItem.get
      id: $state.params.id
    , (response) ->
      $scope.item = response
      $scope.showPhoto = $scope.item.photo
      $scope.editPhoto = not $scope.showPhoto

    $scope.toggleEditPhoto = ->
      $scope.editPhoto = not $scope.editPhoto

    $scope.deletePhoto = ->
      $scope.item.$removePhoto ->
        $scope.item.photo = null
        $scope.showPhoto = false
        $scope.editPhoto = true
        notifier.success "Your photo has been removed"

    api.Place.query().$promise.then (response) ->
      $scope.places = response

    $scope.save = ->
      $scope.item.$update ->
        notifier.success "Your item has been updated"
        $state.go "storage.itemDetail",
          id: $scope.item.id


    $scope.cancel = ->
      $state.go "storage.itemDetail",
        id: $scope.item.id

]).controller("storage.ItemDetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.StorageItem.get
      id: $state.params.id
    , (response) ->
      $scope.item = response

    $scope.deleteItem = ->
      $scope.item.$delete ->
        notifier.success "Your item has been removed"
        $state.go "storage.list"
]).controller("storage.PlaceDetailCtrl", [
  "$scope"
  "$state"
  "api"
  "paginator"
  "notifier"
  ($scope, $state, api, paginator, notifier) ->
    $scope.paginator = paginator()
    api.Place.get
      id: $state.params.id
    , (response) ->
      $scope.place = response
      $scope.paginator.reload $scope.place.items

    $scope.deletePlace = ->
      $scope.place.$delete ->
        notifier.success "Storage area has been removed"
        $state.go "storage.list"

]).controller("storage.EditPlaceCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Place.get
      id: $state.params.id
    , (response) ->
      $scope.place = response

    $scope.save = ->
      $scope.place.$update ->
        notifier.success "The storage area has been updated"
        $state.go "storage.placeDetail",
          id: $scope.place.id


    $scope.cancel = ->
      $state.go "storage.placeDetail",
        id: $scope.place.id

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

]).controller("parking.ListCtrl", [
  "$scope"
  "api"
  "paginator"
  ($scope, api, paginator) ->
    $scope.paginator = paginator()
    api.Vehicle.query().$promise.then (response) ->
      angular.forEach response, (item) ->
        item.searchTerms = item.description + " " + item.registration_number + item.resident.full_name

      $scope.paginator.reload response

]).controller("parking.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.vehicle = new api.Vehicle()
    $scope.save = ->
      $scope.vehicle.$save ->
        notifier.success "Your vehicle has been added"
        $state.go "parking.list"

    $scope.cancel = ->
      $state.go "parking.list"

]).controller("parking.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Vehicle.get
      id: $state.params.id
    , (response) ->
      $scope.vehicle = response

    $scope.deleteVehicle = ->
      $scope.vehicle.$remove ->
        notifier.success "Your vehicle has been removed"
        $state.go "parking.list"

    $scope.save = ->
      $scope.vehicle.$update ->
        notifier.success "Your vehicle has been updated"
        $state.go "parking.detail",
          id: $scope.vehicle.id

    $scope.cancel = ->
      $state.go "parking.detail",
        id: $scope.vehicle.id

]).controller("parking.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Vehicle.get
      id: $state.params.id
    , (response) ->
      $scope.vehicle = response

    $scope.deleteVehicle = ->
      $scope.vehicle.$delete ->
        notifier.success "Your vehicle has been removed"
        $state.go "parking.list"

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

]).controller "account.ChangePasswordCtrl", [
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

]
