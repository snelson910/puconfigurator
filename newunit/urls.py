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
    path("newunit/manual/motors", views.motors, name="motors"),
    path("newunit/manual/pumpnums", views.pumpnums, name="pumpnums"),
    path("newunit/manual/pumpselect", views.pumpselect, name="pumpselect"),
    path("newunit/manual/pumpparts", views.pumpparts, name="pumpparts"),
    path("newunit/details", views.details, name="details"),
    path("newunit/manual/extra", views.extra, name="extra"),
    path("newunit/manual/search", views.search, name="search"),
]