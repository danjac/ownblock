from django.http import HttpResponse, Http404

from rest_framework import viewsets
from rest_framework.decorators import link

from apps.accounts.permissions import IsResidentOrManagerReadOnly


from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):

    model = Document
    serializer_class = DocumentSerializer
    permission_classes = (IsResidentOrManagerReadOnly,)

    @link()
    def download(self, request, pk, *args, **kwargs):
        try:
            obj = self.get_queryset().get(pk=pk)
        except self.model.DoesNotExist():
            raise Http404()

        response = HttpResponse(obj.file, content_type=obj.get_content_type())
        response['Content-Disposition'] = 'attachment; filename=' + \
            obj.get_filename()
        return response

    def get_queryset(self):
        return super().get_queryset().filter(building=self.request.building)
