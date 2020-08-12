from django.urls import path

from . import views


urlpatterns = [
    path("newunit", views.newunit, name="newunit"),
    path("logout", views.logout, name="logout"),
    path("newunit/pumpwizard", views.pumpwizard, name="pumpwizard"),
    path("newunit/manual", views.manual, name="manual"),
    path("newunit/manual/coupling", views.coupling, name="coupling"),
    path("newunit/reservoir", views.reservoir, name="reservoir"),
]