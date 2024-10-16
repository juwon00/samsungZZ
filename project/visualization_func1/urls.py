from django.urls import path
from . import views

# 임의로 확인할 url 생성
urlpatterns = [
    path('congestion/', views.congestion_view, name='congestion_view'),
]
