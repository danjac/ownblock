from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_managers
from django.http import HttpResponseRedirect
from django.template import Context, loader
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Signup
from .forms import SignupForm


class CreateSignup(CreateView):

    template_name = 'signups/form.html'
    model = Signup
    form_class = SignupForm

    def get_success_url(self):
        return reverse('signups:done', [self.object.pk])

    def send_emails(self):

        context = Context({'signup': self.object})

        template = loader.get_template('signups/emails/customer.txt')

        send_mail("Thanks for signing up to Ownblock",
                  template.render(context),
                  settings.DEFAULT_FROM_EMAIL,
                  [self.object.email])

        template = loader.get_template('signups/emails/managers.txt')

        mail_managers("New signup: %s" % self.object.name,
                      template.render(context))

    def form_valid(self, form):
        self.object = form.save()
        self.send_emails()
        return HttpResponseRedirect(self.get_success_url())


class SignupDone(DetailView):

    template_name = 'signups/done.html'
