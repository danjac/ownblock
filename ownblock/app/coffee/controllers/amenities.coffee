angular.module("ownblock.controllers.amenities", [
  "ui.calendar"
  "ownblock"
  "ownblock.services"
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

])
