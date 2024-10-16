from django.db import models

# Create your models here.
class Amenities(models.Model):
    sttn = models.CharField(max_length=100)  # 역명
    line = models.CharField(max_length=20)    # 호선
    cultural_space = models.BooleanField(default=False)  # 문화공간 여부
    wheelchair_lift = models.BooleanField(default=False) # 휠체어 리프트 여부
    meeting_spot = models.BooleanField(default=False)    # 만남의 장소 여부
    parking_lot = models.BooleanField(default=False)     # 환승 주차장 여부
    bike_rack = models.BooleanField(default=False)       # 자전거 보관소 여부
    elevator = models.BooleanField(default=False)        # 엘리베이터 여부
    ticket_office = models.BooleanField(default=False)   # 기차 예매 여부
    civil_service = models.BooleanField(default=False) # 무인 민원 발급기 여부
    currency_exchange = models.BooleanField(default=False)      # 환전 키오스크 여부
    nursing_room = models.BooleanField(default=False)           # 수유실 여부

    def __str__(self):
        return f"{self.sttn} ({self.line})"