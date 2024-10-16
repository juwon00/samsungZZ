from django.urls import path
from .views import SubwayMonthlyPassengerCounterListView

urlpatterns = [
    path(
        "api/subway-monthly-passenger-list/",
        SubwayMonthlyPassengerCounterListView.as_view(),
        name="subway-monthly-passenger-list",
    ),
]
