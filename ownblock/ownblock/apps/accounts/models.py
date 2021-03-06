import urllib
import hashlib

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.core.mail import send_mail
from django.template import Context, loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    _user_has_perm,
)


from factory.fuzzy import FuzzyText

from model_utils import Choices

from ..buildings.models import Apartment

_fuzzier = FuzzyText()


class UserManager(BaseUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def create_user(self, email, first_name, last_name, role,
                    password=None, **kwargs):

        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role,
            **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        return self.create_user(email, first_name,
                                last_name,
                                role='manager',
                                password=password,
                                is_staff=True)


class InactiveUserManager(BaseUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class User(AbstractBaseUser):

    ROLES = Choices('resident', 'manager')

    email = models.EmailField(unique=True, max_length=160)
    original_email = models.EmailField(max_length=160, blank=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    site = models.ForeignKey(Site, null=True, blank=True)

    apartment = models.ForeignKey(Apartment, null=True, blank=True)

    role = models.CharField(choices=ROLES, default='resident', max_length=10)

    objects = UserManager()
    inactive_objects = InactiveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    MODEL_PERMISSIONS = {
        'resident': {
            'amenities.add_booking',
            'amenities.change_booking',
            'amenities.delete_booking',
            'complaints.add_complaint',
            'messaging.add_message',
            'notices.add_notice',
            'notices.change_notice',
            'notices.delete_notice',
            'notices.add_notice',
            'parking.add_vehicle',
            'parking.change_vehicle',
            'parking.delete_vehicle',
            'storage.add_item',
            'storage.change_item',
            'storage.delete_item',
            'tickets.add_ticket',
        },
        'manager': {
            'accounts.add_user',
            'accounts.change_user',
            'accounts.delete_user',
            'amenities.add_amenity',
            'amenities.change_amenity',
            'amenities.delete_amenity',
            'amenities.change_booking',
            'amenities.delete_booking',
            'contacts.add_contact',
            'contacts.change_contact',
            'contacts.delete_contact',
            'documents.add_document',
            'documents.change_document',
            'documents.delete_document',
            'messaging.add_message',
            'notices.add_notice',
            'notices.change_notice',
            'notices.delete_notice',
            'storage.add_place',
            'storage.change_place',
            'storage.delete_place',
            'storage.change_item',
            'storage.delete_item',
            'tickets.add_ticket',
            'tickets.change_ticket',
        },
    }

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    def delete(self, **kwargs):
        """Set active to False, and obfuscate email address to allow re-use."""

        # keep original email address in case we need to re-activate later

        self.original_email = self.email

        self.email = "{0}@{1}".format(_fuzzier.fuzz(), _fuzzier.fuzz())

        self.set_unusable_password()
        self.is_active = False
        self.save()

    def real_delete(self, **kwargs):
        """Actually deletes the user."""
        return super().delete(**kwargs)

    # Hook for custom auth backend
    def has_model_permission(self, perm):
        """Provides model-scpe permissions"""
        return perm in self.MODEL_PERMISSIONS.get(self.role, {})

    # Permission on object itself
    def has_permission(self, user, perm):
        if user.role == 'manager':
            return (self.role == 'resident' and
                    self.apartment and
                    self.apartment.building.site_id ==
                    user.site_id)
        return perm == 'accounts.change_user' and user.id == self.id

    # Hooks for Django admin and Rest Framework
    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, module):
        return self.is_staff

    def get_site(self):
        if self.site_id:
            return self.site
        elif self.apartment_id:
            return self.apartment.building.site
        return Site.objects.get_current()

    def get_gravatar_url(self, size=40):
        return "http://www.gravatar.com/avatar/{0}?{1}".format(
            hashlib.md5(self.email.lower().encode()).hexdigest(),
            urllib.parse.urlencode({'s': size})
        )


def send_invitation_email(sender, instance, created, **kwargs):
    if not created or instance.is_staff:
        return

    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)

    template = loader.get_template('accounts/email/invitation.txt')

    site = instance.get_site()

    message = template.render(Context({
        'uid': uid,
        'token': token,
        'site': site,
        'user': instance,
    })
    )

    send_mail(
        '{}: Invitation to join'.format(site.name),
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email]
    )


def connect_signals():
    """Called by app config"""
    signals.post_save.connect(
        send_invitation_email,
        sender=User,
        dispatch_uid='accounts.send_invitation_email')
