from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class user(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
    )
    email = models.EmailField(_('email address'), blank=True)
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True,
    )
    date_created = models.DateTimeField(
        _('date created'),
        auto_now_add=True,
    )
    is_active = models.NullBooleanField(
        _('active'),
        default=True,
    )
    avatar = models.URLField(
        _('avatar'),
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
            Returns full name
        '''
        return f'{self.first_name} {self.last_name}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
            Send mail to user
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
