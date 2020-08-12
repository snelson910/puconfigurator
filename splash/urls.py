from django.urls import path

from . import views


urlpatterns = [
    path("home", views.splash, name="splash"),
    path("logout", views.logout, name="logout")
]