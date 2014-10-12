angular.module("ownblock", [
  "ngResource"
  "ngSanitize"
  "ngCookies"
  "ui.router"
  "ui.calendar"
  "ui.bootstrap"
  "ownblock.services"
  "ownblock.directives"
  "ownblock.controllers.app"
  "ownblock.controllers.account"
  "ownblock.controllers.amenities"
  "ownblock.controllers.buildings"
  "ownblock.controllers.complaints"
  "ownblock.controllers.contacts"
  "ownblock.controllers.documents"
  "ownblock.controllers.home"
  "ownblock.controllers.residents"
  "ownblock.controllers.messages"
  "ownblock.controllers.notices"
  "ownblock.controllers.parking"
  "ownblock.controllers.storage"
  "ownblock.controllers.tickets"
]).constant(urls:
  static: "/static/"
  partials: "/static/partials/"
  img: "/static/img/"
).config([
  "$httpProvider"
  "$resourceProvider"
  "$stateProvider"
  "$urlRouterProvider"
  "urls"
  ($httpProvider, $resourceProvider, $stateProvider, $urlRouterProvider, urls) ->
    $resourceProvider.defaults.stripTrailingSlashes = true
    $httpProvider.defaults.xsrfCookieName = "csrftoken"
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"
    $httpProvider.interceptors.push ($q, $location, notifier) ->
      responseError: (response) ->
        warning = "Sorry, an error has occurred"
        result = $q.reject(response)
        switch response.status
          when 401, 403
            $location.path "accessdenied"
            return result
          when 404
            $location.path "notfound"
            return result
          when 400
            warning = "Sorry, your form appears to have some errors"
          when 413
            warning = "Sorry, your upload was too large"
        notifier.warning warning  if warning
        $q.reject response

    $httpProvider.defaults.transformRequest = (data, headersGetter) ->
      return data  if data is `undefined`
      fd = new FormData()
      isFileUpload = false
      headers = headersGetter()
      angular.forEach data, (value, key) ->
        if value instanceof FileList
          isFileUpload = true
          if value.length is 1
            fd.append key, value[0]
          else
            angular.forEach value, (file, index) ->
              fd.append key + "_" + index, file
              return

        else
          fd.append key, value
        return

      if isFileUpload
        headers["Content-Type"] = `undefined`
        return fd
      JSON.stringify data

    $stateProvider.state("site",
      abstract: true
      templateUrl: urls.partials + "base.html"
      resolve:
        auth: [
          "auth"
          (auth) ->
            return auth
        ]
    ).state("accessdenied",
      url: "/accessdenied"
      templateUrl: urls.partials + "accessDenied.html"
    ).state("notfound",
      url: "/notfound"
      templateUrl: urls.partials + "notfound.html"
    ).state("account",
      templateUrl: urls.partials + "account/base.html"
      parent: "site"
    ).state("account.edit",
      url: "/account"
      templateUrl: urls.partials + "account/edit.html"
      controller: "account.EditCtrl"
    ).state("account.password",
      url: "/account/pass"
      templateUrl: urls.partials + "account/passwordForm.html"
      controller: "account.ChangePasswordCtrl"
    ).state("residents",
      templateUrl: urls.partials + "residents/base.html"
      parent: "site"
    ).state("residents.list",
      url: "/residents"
      templateUrl: urls.partials + "residents/list.html"
      controller: "residents.ListCtrl"
    ).state("residents.new",
      url: "/residents/new"
      templateUrl: urls.partials + "residents/form.html"
      controller: "residents.NewCtrl"
      data:
        access: "manager"
    ).state("residents.edit",
      url: "/residents/:id/edit"
      templateUrl: urls.partials + "residents/form.html"
      controller: "residents.EditCtrl"
      data:
        access: "manager"
    ).state("residents.detail",
      url: "/residents/:id"
      templateUrl: urls.partials + "residents/detail.html"
      controller: "residents.DetailCtrl"
    ).state("messages",
      templateUrl: urls.partials + "messages/base.html"
      parent: "site"
    ).state("messages.list",
      url: "/messages"
      templateUrl: urls.partials + "messages/list.html"
      controller: "messages.ListCtrl"
    ).state("messages.detail",
      url: "/messages/:id"
      templateUrl: urls.partials + "messages/detail.html"
      controller: "messages.DetailCtrl"
    ).state("messages.send",
      url: "/messages/send/:recipient"
      templateUrl: urls.partials + "messages/form.html"
      controller: "messages.SendCtrl"
    ).state("messages.reply",
      url: "/messages/reply/:parent"
      templateUrl: urls.partials + "messages/form.html"
      controller: "messages.ReplyCtrl"
    ).state("notices",
      templateUrl: urls.partials + "notices/base.html"
      parent: "site"
    ).state("notices.list",
      url: "/notices"
      templateUrl: urls.partials + "notices/list.html"
      controller: "notices.ListCtrl"
    ).state("notices.new",
      url: "/notices/new"
      templateUrl: urls.partials + "notices/form.html"
      controller: "notices.NewCtrl"
    ).state("notices.detail",
      url: "/notices/:id"
      templateUrl: urls.partials + "notices/detail.html"
      controller: "notices.DetailCtrl"
    ).state("notices.edit",
      url: "/notices/:id/edit"
      templateUrl: urls.partials + "notices/form.html"
      controller: "notices.EditCtrl"
    ).state("amenities",
      templateUrl: urls.partials + "amenities/base.html"
      parent: "site"
    ).state("amenities.list",
      url: "/amenities"
      templateUrl: urls.partials + "amenities/list.html"
      controller: "amenities.ListCtrl"
    ).state("amenities.newAmenity",
      url: "/amenities/new"
      templateUrl: urls.partials + "amenities/amenityForm.html"
      controller: "amenities.NewAmenityCtrl"
      data:
        access: "manager"
    ).state("amenities.edit",
      url: "/amenities/:id/edit"
      templateUrl: urls.partials + "amenities/amenityForm.html"
      controller: "amenities.EditAmenityCtrl"
    ).state("amenities.detail",
      url: "/amenities/:id"
      templateUrl: urls.partials + "amenities/detail.html"
      controller: "amenities.DetailCtrl"
    ).state("amenities.newTicket",
      url: "/amenities/:id/ticket"
      templateUrl: urls.partials + "amenities/ticketForm.html"
      controller: "amenities.NewTicketCtrl"
    ).state("amenities.bookingDetail",
      url: "/amenities/bookings/:id"
      templateUrl: urls.partials + "amenities/bookingDetail.html"
      controller: "amenities.BookingDetailCtrl"
    ).state("amenities.editBooking",
      url: "/amenities/bookings/:id/edit"
      templateUrl: urls.partials + "amenities/bookingForm.html"
      controller: "amenities.EditBookingCtrl"
    ).state("amenities.newBooking",
      url: "/amenities/:id/bookings/new"
      templateUrl: urls.partials + "amenities/bookingForm.html"
      controller: "amenities.NewBookingCtrl"
      data:
        access: "resident"
    ).state("complaints",
      templateUrl: urls.partials + "complaints/base.html"
      parent: "site"
    ).state("complaints.list",
      url: "/complaints"
      templateUrl: urls.partials + "complaints/list.html"
      controller: "complaints.ListCtrl"
    ).state("complaints.new",
      url: "/complaints/new"
      templateUrl: urls.partials + "complaints/form.html"
      controller: "complaints.NewCtrl"
      data:
        access: "resident"
    ).state("complaints.detail",
      url: "/complaints/:id"
      templateUrl: urls.partials + "complaints/detail.html"
      controller: "complaints.DetailCtrl"
    ).state("tickets",
      templateUrl: urls.partials + "tickets/base.html"
      parent: "site"
    ).state("tickets.list",
      url: "/tickets"
      templateUrl: urls.partials + "tickets/list.html"
      controller: "tickets.ListCtrl"
    ).state("tickets.new",
      url: "/tickets/new"
      templateUrl: urls.partials + "tickets/form.html"
      controller: "tickets.NewCtrl"
    ).state("tickets.detail",
      url: "/tickets/:id"
      templateUrl: urls.partials + "tickets/detail.html"
      controller: "tickets.DetailCtrl"
    ).state("tickets.edit",
      url: "/tickets/:id/edit"
      templateUrl: urls.partials + "tickets/form.html"
      controller: "tickets.EditCtrl"
    ).state("storage",
      templateUrl: urls.partials + "storage/base.html"
      parent: "site"
    ).state("storage.list",
      url: "/storage"
      templateUrl: urls.partials + "storage/list.html"
      controller: "storage.ListCtrl"
    ).state("storage.newItem",
      url: "/storage/items/new"
      templateUrl: urls.partials + "storage/itemForm.html"
      controller: "storage.NewItemCtrl"
      data:
        access: "resident"
    ).state("storage.newPlace",
      url: "/storage/places/new"
      templateUrl: urls.partials + "storage/placeForm.html"
      controller: "storage.NewPlaceCtrl"
      data:
        access: "manager"
    ).state("storage.itemDetail",
      url: "/storage/:id"
      templateUrl: urls.partials + "storage/itemDetail.html"
      controller: "storage.ItemDetailCtrl"
    ).state("storage.placeDetail",
      url: "/storage/places/:id"
      templateUrl: urls.partials + "storage/placeDetail.html"
      controller: "storage.PlaceDetailCtrl"
    ).state("storage.editItem",
      url: "/storage/:id/edit"
      templateUrl: urls.partials + "storage/itemForm.html"
      controller: "storage.EditItemCtrl"
    ).state("storage.editPlace",
      url: "/storage/places/:id/edit"
      templateUrl: urls.partials + "storage/placeForm.html"
      controller: "storage.EditPlaceCtrl"
      data:
        access: "manager"
    ).state("documents",
      templateUrl: urls.partials + "documents/base.html"
      parent: "site"
    ).state("documents.list",
      url: "/docs"
      templateUrl: urls.partials + "documents/list.html"
      controller: "documents.ListCtrl"
    ).state("documents.upload",
      url: "/docs/upload"
      templateUrl: urls.partials + "documents/form.html"
      controller: "documents.UploadCtrl"
      data:
        access: "manager"
    ).state("documents.detail",
      url: "/docs/:id"
      templateUrl: urls.partials + "documents/detail.html"
      controller: "documents.DetailCtrl"
    ).state("parking",
      templateUrl: urls.partials + "parking/base.html"
      parent: "site"
    ).state("parking.list",
      url: "/parking"
      templateUrl: urls.partials + "parking/list.html"
      controller: "parking.ListCtrl"
    ).state("parking.new",
      url: "/parking/new"
      templateUrl: urls.partials + "parking/vehicleForm.html"
      controller: "parking.NewCtrl"
    ).state("parking.detail",
      url: "/parking/:id"
      templateUrl: urls.partials + "parking/detail.html"
      controller: "parking.DetailCtrl"
    ).state("parking.edit",
      url: "/parking/:id/edit"
      templateUrl: urls.partials + "parking/vehicleForm.html"
      controller: "parking.EditCtrl"
    ).state("contacts",
      templateUrl: urls.partials + "contacts/base.html"
      parent: "site"
    ).state("contacts.list",
      url: "/contacts"
      templateUrl: urls.partials + "contacts/list.html"
      controller: "contacts.ListCtrl"
    ).state("contacts.new",
      url: "/contacts/new"
      templateUrl: urls.partials + "contacts/form.html"
      controller: "contacts.NewCtrl"
      data:
        access: "manager"
    ).state("contacts.detail",
      url: "/contacts/:id"
      templateUrl: urls.partials + "contacts/detail.html"
      controller: "contacts.DetailCtrl"
    ).state("contacts.edit",
      url: "/contacts/:id/edit"
      templateUrl: urls.partials + "contacts/form.html"
      controller: "contacts.EditCtrl"
      data:
        access: "manager"
    ).state("buildings",
      templateUrl: urls.partials + "buildings/base.html"
      parent: "site"
    ).state("buildings.list",
      url: "/building/list"
      templateUrl: urls.partials + "buildings/list.html"
      controller: "buildings.ListCtrl"
      data:
        acess: "manager"
    ).state("buildings.apartment",
      url: "/building/:id"
      templateUrl: urls.partials + "buildings/detail.html"
      controller: "buildings.DetailCtrl"
    ).state("buildings.detail",
      url: "/building"
      templateUrl: urls.partials + "buildings/detail.html"
      controller: "buildings.DetailCtrl"
    ).state "home",
      url: "/"
      templateUrl: urls.partials + "home.html"
      parent: "site"
      controller: "HomeCtrl"

    $urlRouterProvider.otherwise "/"
]).run [
  "$rootScope"
  "$state"
  "auth"
  ($rootScope, $state, auth) ->

    # fetch the current user from the session. If the user is not logged in,
    # redirect to the external login page; otherwise sync user details with the 
    # application.
    $rootScope.$on "$stateChangeStart", (event, toState) ->
      unless auth.authorize(toState)
        event.preventDefault()
        $state.transitionTo "accessdenied"

]
