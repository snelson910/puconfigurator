from django.urls import path

from . import views


urlpatterns = [
    path("newunit", views.newunit, name="newunit"),
    path("logout", views.logout, name="logout"),
    path("newunit/pumpwizard", views.pumpwizard, name="pumpwizard"),
    path("newunit/manual", views.manual, name="manual"),
    path("newunit/manual/coupling", views.coupling, name="coupling"),
    path("newunit/manual/pumps", views.pumps, name="pumps"),
    path("newunit/manual/reservoirs", views.reservoirs, name="reservoirs"),
]