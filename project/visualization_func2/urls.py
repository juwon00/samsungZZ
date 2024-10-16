from django.urls import path
from .views import subway_passenger_graph

urlpatterns = [
    path('graph/', subway_passenger_graph, name='subway_passenger_graph'),
]