
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import APIs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', APIs.as_view(), name="apis_view"),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('core.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

