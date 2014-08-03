from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView


class LoginView(FormView):

    """
    Handles login. Redirect post-login depends on user role.
    """

    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        """Exact URLs tbd"""
        if self.request.user.is_staff:
            return reverse('admin:index')
        if self.request.user.role == 'manager':
            return reverse('buildings:select_building')
        return reverse('mainapp')

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.set_test_cookie()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        self.set_test_cookie()
        return self.form_invalid(form)
