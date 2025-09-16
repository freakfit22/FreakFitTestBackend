from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('customers.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_ROOT, documents_root= settings.STATIC_ROOT)