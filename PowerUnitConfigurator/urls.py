from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('splash.urls')),
    path('', include('newunit.urls')),
    path('', include('manifold.urls')),
    path('', include('customers.urls'))
]
