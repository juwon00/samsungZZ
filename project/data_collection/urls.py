from django.urls import path
from .views import SubwayMonthlyPassengerCounterListView, SubwayStationLatLngListView

urlpatterns = [
    path(
        "api/subway-monthly-passenger-list/",
        SubwayMonthlyPassengerCounterListView.as_view(),
        name="subway-monthly-passenger-list",
    ),
    path(
        "api/subway-station-lat-lng-list/",
        SubwayStationLatLngListView.as_view(),
        name="subway-station-lat-lng-list",
    ),
]
