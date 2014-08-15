from django.contrib import admin

from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    raw_id_fields = ('building', )


admin.site.register(Document, DocumentAdmin)
