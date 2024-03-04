from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.views import RegisterView

from nipps_hms.permission import (IsAuthenticatedAccountsRecord,
                                  IsAuthenticatedDoctor,
                                  IsAuthenticatedNurse,
                                  IsAuthenticatedPharmacist,
                                  IsAuthenticatedLabTechnician,
                                  )
from .models import  User
from .utils import Helper


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
    

