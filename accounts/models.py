import string
import random
import pytz
from datetime import datetime, timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from nipps_hms.utils import generate_slug_code

OTP_LENGTH = 6

PENDING = "Pending"
APPROVED = "Approved"
DENIED = "Denied"
INSUFFICIENT = "Insufficient"

STATUS_CHOICES = ((PENDING, "Pending"), (APPROVED, "Approved"),
                      (DENIED, "Denied"), (INSUFFICIENT, "Insufficient"),)

def check_existing_phone(phone_number):
    """A function to check if phone exist. """
   
    if User.objects.filter(phone_number=phone_number).exists():
        raise ValidationError(_(f"User with this phone number '{phone_number}' already exist"))
   

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    
    username = None
    slug = models.SlugField(editable=False)
    email = models.EmailField(_("email address"), unique=True)
    send_password = models.CharField(max_length=64, null=True, blank=True)
    is_profile_completed = models.BooleanField(default=False)
    
    is_active = models.BooleanField(_("Is active"), default=True)

    is_nurse = models.BooleanField(_("Is Nurse"), default=False)
    is_doctor = models.BooleanField(_("Is Doctor"), default=False)
    is_lab_technician = models.BooleanField(_("Is Lab Technician"), default=False)
    is_pharmacist = models.BooleanField(_("Is Phamacist"), default=False)
    is_account = models.BooleanField(_("Is Accountant"), default=False)

    fcm_device_registered = models.BooleanField(default=False)
    
    is_staff = models.BooleanField(_("Staff?"), default=False)
    is_superuser = models.BooleanField(_("Superuser?"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    
def _generate_code(length=OTP_LENGTH):
    characters = string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    return code
