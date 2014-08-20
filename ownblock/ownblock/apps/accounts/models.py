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


from model_utils import Choices


from apps.organizations.models import Organization
from apps.buildings.models import Apartment


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, role, password=None):

        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role, password):
        return self.create_user(email, first_name,
                                last_name,
                                role=role,
                                password=password,
                                is_staff=True)


class User(AbstractBaseUser):

    ROLES = Choices('resident', 'manager')

    email = models.EmailField(unique=True, max_length=160)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    organization = models.ForeignKey(Organization, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, null=True, blank=True)

    role = models.CharField(choices=ROLES, default='resident', max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    MODEL_PERMISSIONS = {
        'resident': {
            'amenities.add_booking',
            'amenities.delete_booking',
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
        },
        'manager': {
            'accounts.add_user',
            'amenities.add_amenity',
            'amenities.delete_booking',
            'documents.add_document',
            'documents.change_document',
            'documents.delete_document',
            'notices.add_notice',
            'notices.change_notice',
            'notices.delete_notice',
            'storage.add_place',
        },
    }

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    # Hook for custom auth backend

    def has_model_permission(self, perm):
        """Provides model-scpe permissions"""
        return perm in self.MODEL_PERMISSIONS.get(self.role, {})

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


def send_invitation_email(sender, instance, created, **kwargs):
    if not created:
        return

    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)
    site = Site.objects.get_current()

    template = loader.get_template('accounts/email/invitation.txt')

    message = template.render(Context({
        'uid': uid,
        'token': token,
        'site': site,
        'user': instance,
    })
    )

    send_mail(
        '%s:Invitation to join' % site.name,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email]
    )


signals.post_save.connect(send_invitation_email, sender=User,
                          dispatch_uid='accounts.send_invitation_email')
