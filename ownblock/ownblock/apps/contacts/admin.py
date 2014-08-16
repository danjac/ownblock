from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):

    raw_id_fields = ('building', )
    list_display = ('name', 'building')


admin.site.register(Contact, ContactAdmin)
