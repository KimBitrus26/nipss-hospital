
from django.urls import path, include
from .views import (CustomRegisterView, 
                    )


urlpatterns = [
    
    path('auth/', include('dj_rest_auth.urls')),
    path("auth/registration/", CustomRegisterView.as_view(), name="signup"),
]
