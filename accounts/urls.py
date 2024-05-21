
from django.urls import path, include
from .views import (CustomRegisterView, CustomLoginView,
                    CreateFCMDeviceView,
                    )


urlpatterns = [
    
    path('auth/', include('dj_rest_auth.urls')),
    path("auth/registration/", CustomRegisterView.as_view(), name="signup"),
    path("auth/custom-login/", CustomLoginView.as_view(), name="custom_login"),
    path("auth/connect-device/", CreateFCMDeviceView.as_view(), name="connect_device"),
]
