from django.urls import path
from . import views


urlpatterns = [
    path("manifold", views.manifold, name="manifold"),
    path("logout", views.logout, name="logout"),
    path("manifold/stations", views.stations, name="stations"),
    path("manifold/bom", views.bom, name="bom"),
    path("manifold/download/", views.download, name="download"),
]