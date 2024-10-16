from django.db import models

# Create your models here.

class DegreeOfSubwayCongestion(models.Model):
    sub_name = models.CharField(max_length=20)  # 지하철역 이름
    sub_num = models.IntegerField() # 지하철역 번호
    route_name = models.CharField(max_length=20)    # 노선명
    weekday = models.CharField(max_length=10)  # 요일 구분
    time = models.CharField(max_length=10)  # 시간대 구분
    congestion = models.FloatField(null=True)    # 혼잡도
    
    def __str__(self):
        return f"{self.sub_name} - {self.route_name} - {self.time}"