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

]).controller("buildings.ListCtrl", [
  "$scope"
  "$state"
  "api"
  "auth"
  ($scope, $state, api, auth) ->
    getCity = (city) ->
      rv = null
      angular.forEach $scope.cities, (value) ->
        if value.name is city
          rv = value

      if rv is null
        rv =
          name: city
          buildings: []

        $scope.cities.push rv
      rv
    $scope.cities = []
    api.Building.query().$promise.then (response) ->
      angular.forEach response, (building) ->
        city = getCity(building.city)
        city.buildings.push building


    $scope.selectBuilding = (building) ->
      api.Building.get
        id: building.id
      , (response) ->
        auth.user.building = response
        $state.go "buildings.detail"

]).controller("buildings.DetailCtrl", [
  "$scope"
  "$state"
  "$window"
  "$modal"
  "api"
  "auth"
  "urls"
  ($scope, $state, $window, $modal, api, auth, urls) ->
    apartmentId = null
    showApartment = false
    if $state.params.id
      apartmentId = parseInt($state.params.id, 10)
      showApartment = true
    else apartmentId = auth.user.apartment  if auth.user.apartment
    $scope.apartmentSelector = id: apartmentId
    $scope.building = $scope.auth.user.building
    mapCreated = false
    $scope.generateMap = ->
      return  if mapCreated
      OL = $window.OpenLayers
      map = new OL.Map("map",
        controls: [
          new OL.Control.Navigation()
          new OL.Control.PanZoomBar()
          new OL.Control.ScaleLine()
          new OL.Control.MousePosition()
          new OL.Control.Permalink()
          new OL.Control.Attribution()
        ]
        maxExtent: new OL.Bounds(-180, -90, 180, 90)
        displayProjection: new OL.Projection("EPSG:4326")
        maxResolution: "auto"
      )
      fromProjection = new OL.Projection("EPSG:4326")
      toProjection = new OL.Projection("EPSG:900913")
      layer = new OL.Layer.OSM()
      point = new OL.LonLat($scope.building.longitude, $scope.building.latitude).transform(fromProjection, toProjection)
      markers = new OL.Layer.Markers("Markers")
      size = new OL.Size(21, 25)
      offset = new OL.Pixel(-(size.w / 2), -size.h)
      icon = new OL.Icon(urls.img + "marker.png", size, offset)
      map.addLayer layer
      map.addLayer markers
      map.setCenter point, 16
      markers.addMarker new OL.Marker(point, icon)
      mapCreated = true

    $scope.apartments = []
    $scope.tabs =
      building:
        active: true

      apartments:
        active: false

    $scope.tabs.apartments.active = true  if showApartment
    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.selectApartment = ->
      unless $scope.apartmentSelector.id
        $scope.currentApartment = null

      api.Apartment.get
        id: $scope.apartmentSelector.id
      , (response) ->
        $scope.currentApartment = response

    $scope.selectApartment()
    $scope.addResident = (apartment) ->
      modalInstanceCtrl = ($scope, $modalInstance) ->
        $scope.resident = {}
        $scope.cancel = ->
          $modalInstance.dismiss "cancel"

        $scope.save = ->
          $modalInstance.close $scope.resident

      modalInstance = $modal.open(
        templateUrl: urls.partials + "buildings/modalResidentForm.html"
        controller: modalInstanceCtrl
      )
      modalInstance.result.then (resident) ->
        api.Apartment.addResident(
          id: apartment.id
        , resident).$promise.then (response) ->
          $scope.currentApartment.users.push response

]).controller("residents.ListCtrl", [
  "$scope"
  "api"
  "auth"
  "paginator"
  ($scope, api, auth, paginator) ->
    $scope.user = auth.user
    $scope.paginator = paginator()
    api.Resident.query(residents: true).$promise.then (response) ->
      $scope.paginator.reload response

]).controller("residents.NewCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.resident = new api.Resident()
    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.resident.$save (->
        notifier.success "The resident has been added"
        $state.go "residents.list"
      ), (response) ->
        $scope.serverErrors = response.data
      $scope.cancel = ->
      $state.go "residents.list"
]).controller("residents.EditCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Resident.get
      id: $state.params.id
    , (response) ->
      $scope.resident = response

    api.Apartment.query().$promise.then (response) ->
      $scope.apartments = response

    $scope.save = ->
      $scope.resident.$update (->
        notifier.success "The resident has been updated"
        $state.go "residents.detail",
          id: $scope.resident.id

      ), (response) ->
        $scope.serverErrors = response.data
    $scope.cancel = ->
      $state.go "residents.detail",
        id: $scope.resident.id

]).controller("residents.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Resident.get
      id: $state.params.id
    , (response) ->
      $scope.resident = response

    $scope.deleteUser = ->
      $scope.resident.$delete ->
        notifier.success $scope.resident.full_name + " has been removed."
        $state.go "residents.list"

]).controller("amenities.ListCtrl", [
  "$scope"
  "api"
  "notifier"
  "paginator"
  "auth"
  ($scope, api, notifier, paginator, auth) ->
    $scope.paginator = paginator()
    $scope.cols = [
      "Amenity"
      "Status"
    ]
    $scope.cols.push ""  if auth.hasRole("resident")
    api.Amenity.query().$promise.then (response) ->
      $scope.paginator.reload response

]).controller("amenities.NewAmenityCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    $scope.amenity = new api.Amenity(is_available: true)
    $scope.save = ->
      $scope.amenity.$save ->
        notifier.success "Amenity has been added"
        $state.go "amenities.list"
      $scope.cancel = ->
      $state.go "amenities.list"

]).controller("amenities.EditAmenityCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Amenity.get
      id: $state.params.id
    , (response) ->
      $scope.amenity = response

    $scope.save = ->
      $scope.amenity.$update ->
        notifier.success "Amenity has been updated"
        $state.go "amenities.detail",
          id: $scope.amenity.id

      $scope.cancel = ->
      $state.go "amenities.detail",
        id: $scope.amenity.id

]).controller("amenities.NewBookingCtrl", [
  "$scope"
  "$state"
  "$stateParams"
  "api"
  ($scope, $state, $stateParams, api) ->
    api.Amenity.get(id: $stateParams.id).$promise.then (response) ->
      $scope.amenity = response
      now = new Date()
      reservedFrom = new Date()
      reservedTo = new Date()
      reservedFrom.setHours now.getHours() + 1
      reservedTo.setHours now.getHours() + 2
      $scope.now = now
      $scope.booking = new api.Booking(
        amenity: $scope.amenity.id
        reserved_from: reservedFrom
        reserved_to: reservedTo
      )

    $scope.timepickerOptions =
      showMeridian: false
      disabled: false

    $scope.datepickerOptions =
      disabled: false
      dateFormat: "dd/mm/yyyy"

    $scope.save = ->
      $scope.booking.$save (->
        $state.go "amenities.detail",
          id: $stateParams.id

      ), (response) ->
        $scope.serverErrors = response.data

]).controller("amenities.EditBookingCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Booking.get
      id: $state.params.id
    , (response) ->
      $scope.now = new Date()
      $scope.booking = response

    $scope.save = ->
      $scope.booking.$update (->
        $state.go "amenities.detail",
          id: $scope.booking.amenity

        notifier.success "Your booking has been updated"
      ), (response) ->
        $scope.serverErrors = response.data
    $scope.timepickerOptions =
      showMeridian: false
      disabled: false

    $scope.datepickerOptions =
      disabled: false
      dateFormat: "dd/mm/yyyy"
]).controller("amenities.BookingDetailCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Booking.get
      id: $state.params.id
    , (response) ->
      $scope.booking = response

    $scope.cancelBooking = ->
      $scope.booking.$delete ->
        notifier.success "The booking has been canceled"
        $state.go "amenities.detail",
          id: $scope.booking.amenity

]).controller("amenities.NewTicketCtrl", [
  "$scope"
  "$state"
  "api"
  "notifier"
  ($scope, $state, api, notifier) ->
    api.Amenity.get
      id: $state.params.id
    , (response) ->
      $scope.amenity = response
      $scope.ticket = new api.Ticket(amenity: $scope.amenity.id)
      return

    $scope.save = ->
      $scope.ticket.$save ->
        notifier.success "Thanks for reporting the issue!"
        $state.go "amenities.detail",
          id: $state.params.id

    $scope.cancel = ->
      $state.go "amenities.detail",
        id: $state.params.id

]).controller("amenities.DetailCtrl", [
  "$scope"
  "$state"
  "api"
  "auth"
  "notifier"
  "paginator"
  ($scope, $state, api, auth, notifier, paginator) ->
    getColor = (residentId, isPast) ->
      return "#555"  if isPast
      (if auth.user.id is residentId then "#800" else "#008")
    formatTime = (dt) ->
      hours = dt.getHours()
      mins = dt.getMinutes()
      ((if hours < 10 then "0" + hours else hours)) + ":" + ((if mins < 10 then "0" + mins else mins))
    showBooking = (booking) ->
      $state.go "amenities.bookingDetail",
        id: booking.id

    bookings = []
    today = new Date()
    $scope.paginator = paginator()
    $scope.eventSources = [bookings]
    $scope.deleteAmenity = ->
      $scope.amenity.$delete ->
        notifier.success "The amenity has been removed"
        $state.go "amenities.list"

    api.Amenity.get(id: $state.params.id).$promise.then (response) ->
      $scope.amenity = response
      $scope.bookings = []
      angular.forEach $scope.amenity.bookings, (booking, counter) ->
        reservedFrom = new Date(booking.reserved_from)
        reservedTo = new Date(booking.reserved_to)
        title = formatTime(reservedFrom) + " - " + formatTime(reservedTo)
        isPast = reservedFrom < today
        color = getColor(booking.resident, isPast)
        bookings.push
          start: reservedFrom
          end: reservedTo
          color: color
          title: title
          data: booking
          index: counter


      $scope.paginator.reload $scope.amenity.tickets

    $scope.uiConfig = calendar:
      height: 450
      editable: false
      header:
        left: "basicDay basicWeek month"
        center: "title"
        right: "today prev,next"

      eventClick: (calEvent) ->
        showBooking calEvent.data

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
