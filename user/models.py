from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather not Say', 'Rather not Say'),
)


class user(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
    )

    email = models.EmailField(
        _('email address'),
        blank=True,
    )

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
        default=timezone.now,
    )

    avatar = models.URLField(
        _('avatar'),
        blank=True,
    )

    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        default='Male',
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
    )

    is_staff = models.BooleanField(
        _('staff'),
        default=False,
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
