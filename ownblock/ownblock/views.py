import json

from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .apps.accounts.serializers import AuthUserSerializer


class AppView(TemplateView):
    template_name = 'app.html'

    def get(self, request, *args, **kwargs):
        if request.building:
            return super().get(request, *args, **kwargs)
        if request.user.is_staff:
            redirect_url = reverse('admin:index')
        else:
            redirect_url = reverse('index')
        return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # bootstrap data
        user_data = AuthUserSerializer(self.request.user,
                                       context={'request': self.request}).data

        user_data['site_name'] = self.request.site.name
        context['user_data'] = json.dumps(user_data)
        return context


class ContactForm(forms.Form):
    name = forms.CharField()
    question = forms.CharField(required=False)
    email = forms.EmailField()


class ContactView(FormView):

    form_class = ContactForm
    template_name = "contact.html"

    def form_valid(self, form):

        message = """
        Someone has asked a question:

        Name: %(name)s
        Email: %(email)s
        Question:
        %(question)s
        """ % form.cleaned_data
        mail_admins("Contact message", message)

        return HttpResponseRedirect(self.request.path + "?sent=1")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent'] = 'sent' in self.request.GET
        return context
