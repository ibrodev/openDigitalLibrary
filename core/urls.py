from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('odlauth.urls')),
    path('library/', include('library.urls')),
    path("", index, name="index")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)