from django.urls import path
from . import views


urlpatterns = [
    path("pumpmotor", views.pumpmotor, name="pumpmotor"),
    path("logout", views.logout, name="logout"),
    path("pumpmotor/coupling", views.coupling, name="coupling"),
]