from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

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
    