angular.module("ownblock.services", ["ngResource"]).service("auth", [->
  authorize: (state) ->
    data = state.data or {}
    access = data.access or null
    @hasRole access

  hasRole: (access) ->
    return true  unless access
    @user and @user.role is access

  sync: (response) ->
    @user = response

  update: (response) ->
    @user.first_name = response.first_name
    @user.last_name = response.last_name
    @user.email = response.email
    @user.full_name = response.full_name

]).factory("notifier", [
  "$rootScope"
  ($rootScope) ->
    Notifier = ->
      @notifications = []

    Notifier::notify = (type, msg) ->
      notification =
        type: type
        message: msg

      $rootScope.$broadcast "Notifier.new", notification
      @notifications.push notification

    Notifier::dismiss = (index) ->
      @notifications.splice index, 1

    Notifier::remove = (notification) ->
      index = @notifications.indexOf(notification)
      @dismiss index

    Notifier::success = (msg) ->
      @notify "success", msg

    Notifier::warning = (msg) ->
      @notify "warning", msg
      return

    Notifier::info = (msg) ->
      @notify "info", msg

    Notifier::danger = (msg) ->
      @notify "danger", msg

    return new Notifier()

]).factory("paginator", [
  "$filter"
  ($filter) ->
    Paginator = (items, maxSize) ->
      @maxSize = maxSize or 10
      @reload items

    Paginator::change = ->
      offset = (@page - 1) * @maxSize
      @currentItems = @filteredItems.slice(offset, offset + @maxSize)
      @isEmpty = @currentItems.length is 0

    Paginator::reload = (items) ->
      @items = @filteredItems = items or []
      @total = @items.length
      @page = 1
      @change()

    Paginator::filter = (value) ->
      if value
        @filteredItems = $filter("filter")(@items, value)
      else
        @filteredItems = @items
      @total = @filteredItems.length
      @change()

    Paginator::remove = (index) ->
      @items.splice index, 1
      @items.total = @items.length
      @change()

    return (items, maxSize) ->
      new Paginator(items, maxSize)

]).service "api", [
  "$resource"
  ($resource) ->
    makeEndpoint = (url, actions) ->
      unless angular.isDefined(actions)
        actions = update:
          method: "PUT"
      $resource url,
        id: "@id"
      , actions
    return (
      Notice: makeEndpoint("/api/notices/notices/:id")
      Message: makeEndpoint("/api/messages/messages/:id")
      Resident: makeEndpoint("/api/users/people/:id")
      Amenity: makeEndpoint("/api/amenities/items/:id")
      Booking: makeEndpoint("/api/amenities/bookings/:id")
      Place: makeEndpoint("/api/storage/places/:id")
      Document: makeEndpoint("/api/documents/documents/:id")
      Contact: makeEndpoint("/api/contacts/contacts/:id")
      Vehicle: makeEndpoint("/api/parking/vehicles/:id")
      Complaint: makeEndpoint("/api/complaints/complaints/:id")
      Ticket: makeEndpoint("/api/tickets/tickets/:id")
      StorageItem: makeEndpoint("/api/storage/items/:id",
        removePhoto:
          url: "/api/storage/items/:id/remove_photo"
          method: "PATCH"

        update:
          method: "PUT"
      )
      Apartment: makeEndpoint("/api/buildings/apartments/:id",
        addResident:
          url: "/api/buildings/apartments/:id/add_resident"
          method: "POST"
      )
      Building: makeEndpoint("/api/buildings/buildings/:id")
      Timeline: $resource("/api/buildings/timeline")
      Auth: $resource("/api/users/auth/", {},
        update:
          method: "PUT"

        changePassword:
          method: "PATCH"
      )
    )
]
