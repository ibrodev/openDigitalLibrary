from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('odlauth.urls')),
    path("", index, name="index")
]