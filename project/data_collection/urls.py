from django.urls import path
from .views import SubwayMonthlyPassengerCounterListView, DegreeOfSubwayCongestionListView

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
    )
]
