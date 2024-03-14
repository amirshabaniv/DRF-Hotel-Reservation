from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path('', include('accounts.urls')),
    path('', include('hotels.urls')),
    path('', include('carts.urls')),
]