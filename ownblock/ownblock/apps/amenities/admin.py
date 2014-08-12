from django.contrib import admin


from .models import Amenity


class AmenityAdmin(admin.ModelAdmin):

    raw_id_fields = ('building', )


admin.site.register(Amenity, AmenityAdmin)
