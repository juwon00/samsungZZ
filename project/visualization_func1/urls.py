from django.urls import path
from .views import congestion_view

# 임의로 확인할 url 생성
urlpatterns = [
    path('congestion/', congestion_view, name='congestion_view'),
]
