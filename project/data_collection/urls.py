from django.urls import path
from .views import (
    SubwayMonthlyPassengerCounterListView,
    DegreeOfSubwayCongestionListView,
    SubwayDailyPassengerDifferenceView,
    SubwayAmenitiesView,
    SubwayStationLatLngListView,
)


urlpatterns = [
    path(
        "api/subway-monthly-passenger-list/",
        SubwayMonthlyPassengerCounterListView.as_view(),
        name="subway-monthly-passenger-list",
    ),
    path(
        "api/degree-of-subway-congestion-list/",
        DegreeOfSubwayCongestionListView.as_view(),
        name="degree-of-subway-congestion-list",
    ),
    path(
        "api/subway-daily-passenger-difference/<str:date>/<str:line>/<str:sttn>/<str:time_slot>/",
        SubwayDailyPassengerDifferenceView.as_view(),
    ),
    path("api/subway-amenities/<str:line>/<str:sttn>/", SubwayAmenitiesView.as_view()),
    path(
        "api/subway-station-lat-lng-list/",
        SubwayStationLatLngListView.as_view(),
        name="subway-station-lat-lng-list",
    ),
]
