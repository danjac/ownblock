from django import forms

from .models import Signup


class SignupForm(forms.ModelForm):

    class Meta:
        model = Signup
        fields = ('name',
                  'contact_name',
                  'email',
                  'domain',
                  'phone',
                  'num_buildings',
                  'num_apartments',
                  'questions',
                  )

    def clean_domain(self):
        domain = self.cleaned_data['domain']
        return domain.lower()
