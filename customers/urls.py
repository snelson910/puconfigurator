from django.urls import path
from . import views
from .views import SearchResultsView, HomePageView


urlpatterns = [
    path("customers", HomePageView.as_view(), name="customers"),
    path("logout", views.logout, name="logout"),
    path("customers/search-results", SearchResultsView.as_view(), name='search'),
]