from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('med.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
]
