from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.template import Context, loader

from rest_framework import viewsets, parsers
from rest_framework.decorators import link

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):

    model = Document
    serializer_class = DocumentSerializer
    parser_classes = (parsers.MultiPartParser, )

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

    def pre_save(self, obj):
        obj.building = self.request.building

    def post_save(self, obj, created):
        if not created:
            return
        site = self.request.site
        template = loader.get_template('documents/email/new_document.txt')
        for resident in self.request.building.get_residents():
            send_mail('%s: a document has been uploaded',
                      template.render(Context({
                          'resident': resident,
                          'site': site,
                          'document': obj,
                      })),
                      settings.DEFAULT_FROM_EMAIL,
                      [resident.email]
                      )

    def get_queryset(self):
        return super().get_queryset().filter(
            building=self.request.building
        ).order_by('-created')
