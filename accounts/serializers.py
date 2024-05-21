from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.utils.html import strip_tags
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError

from .user_password import CustomPasswordResetForm

from .models import User, OTP_LENGTH


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for custom user objects."""

    class Meta:
        model = User
        fields = ["slug", "email", 
                   "is_profile_completed", "is_nurse", 
                   "is_pharmacist", "is_lab_technician", "is_doctor",
                   "is_account"
                   ]
        read_only_fields = ("email",)
        

class CustomRegisterSerializer(RegisterSerializer):
    """Serializer for custom registeration."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(min_length=8, max_length=18,)
    country_code = serializers.CharField(min_length=3, max_length=4,)

    def __init__(self, *args, **kwargs):
        
        self.fields.pop('password1')
        self.fields.pop('password2')
        self.fields.pop('username')

        super().__init__(*args, **kwargs)

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
       

class CustomLoginSerializer(LoginSerializer): 

    """Serializer for login."""
    
    def _validate_email(self, email, password):
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Unable to log in with the provided credentials")
            user = self.authenticate(email=email, password=password)
        else: 
            raise serializers.ValidationError('Must include "email" and "password".')
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')


class FCMDeviceSerializer(serializers.Serializer):
    registration_token = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = CustomPasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)

        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'subject_template_name': 'registration/password_reset_subject2.txt',
            'email_template_name': 'registration/send_forgot_password_email.html',
        }
        self.reset_form.save(**opts)


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):

        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode as uid_decoder

        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()

    