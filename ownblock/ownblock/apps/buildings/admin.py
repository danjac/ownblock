from django.contrib import admin


from .models import Building, Apartment


class ApartmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('building', )
    list_display = ('building', 'number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()


admin.site.register(Building)
admin.site.register(Apartment, ApartmentAdmin)
