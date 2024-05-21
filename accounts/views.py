from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.views import RegisterView, LoginView, CreateAPIView

from nipps_hms.permission import (IsAuthenticatedAccountsRecord,
                                  IsAuthenticatedDoctor,
                                  IsAuthenticatedNurse,
                                  IsAuthenticatedPharmacist,
                                  IsAuthenticatedLabTechnician,
                                  )
from .models import  User
from .utils import Helper
from .serializers import FCMDeviceSerializer


class CustomLoginView(LoginView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        if self.serializer.is_valid():
            self.login()
            return self.get_response()
            
        error_message = None
       
        if "non_field_errors" in self.serializer.errors.keys():
            error_message = f"{self.serializer.errors['non_field_errors'][0]}"
       
        return Response({"message": error_message, "data": None, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView):
    permission_classes = (AllowAny, )
   
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        user_data = {
            "slug": data["user"]["slug"],
            "email": data["user"]["email"],
            "role": "Agent",
           
        }
        #customise response here
        response_data = {
            "message": "User created successfully.",
            'user': user_data
            }

        if response_data:
            response = Response(
                response_data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response
    

class CreateFCMDeviceView(CreateAPIView):
    permission_classes = (IsAuthenticatedDoctor | IsAuthenticatedLabTechnician | IsAuthenticatedAccountsRecord | IsAuthenticatedNurse | IsAuthenticatedPharmacist,)
   
    serializer_class = FCMDeviceSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            registration_token = serializer.validated_data["registration_token"]
           
            try:
                user = User.objects.get(slug=user.slug)
            except User.DoesNotExist:
                return Response({"message":"No user with this slug exists", "data": None, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            from fcm_django.models import FCMDevice

            device_exists = FCMDevice.objects.filter(user=user.id)

            if device_exists:
                device_exists.delete()

            try:
                FCMDevice.objects.create(
                    user=user, 
                    registration_id=registration_token,
                    type="web"
                    )
            except Exception as e:
                return Response({"message": "An error occured, please try again", "data": None, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            user.fcm_device_registered = True
            user.save()

            return Response({"message": "Device added successfully", "data": None}, status=status.HTTP_201_CREATED)
        
        error_message = None
       
        if "non_field_errors" in serializer.errors.keys():
            error_message = f"{serializer.errors['non_field_errors'][0]}"
       
        return Response({"message": error_message, "data": None, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
