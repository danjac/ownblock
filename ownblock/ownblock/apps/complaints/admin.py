from django.contrib import admin

from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):

    raw_id_fields = ('building', 'apartment', 'resident')
    list_display = ('building', 'complaint_summary')

    def complaint_summary(self, obj):
        return obj.complaint[:50]


admin.site.register(Complaint, ComplaintAdmin)
