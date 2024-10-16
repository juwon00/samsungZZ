from django.urls import path
from .views import SubwayMonthlyPassengerCounterListView, DegreeOfSubwayCongestionListView, SubwayDailyPassengerDifferenceView


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
        'api/subway-daily-passenger-difference/<str:date>/<str:line_number>/<str:station_name>/<str:time_slot>/', 
        SubwayDailyPassengerDifferenceView.as_view(),
    ),
]
