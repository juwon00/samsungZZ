from django.urls import path
from . import views

urlpatterns = [
    #path('search/', views.station_search, name='station_search'),
    path('station-information/', views.subway_passenger_graph, name='subway_passenger_graph'),
]