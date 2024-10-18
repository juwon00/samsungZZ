from django import forms
from data_collection.models import DegreeOfSubwayCongestion

# 드롭다운 필드 정의
class congestionForm(forms.Form):
    # 노선 선택 드롭다운 필드
    LINE_CHOICES = [
        (route_name, route_name) for route_name in DegreeOfSubwayCongestion.objects.values_list('route_name', flat=True).distinct()
    ]
    route_name = forms.ChoiceField(label='호선 선택', choices=LINE_CHOICES)

    # 요일 선택 드롭다운 필드
    week = forms.ChoiceField(
        choices=[
            ("평일", "평일"),
            ("토요일", "토요일"),
            ("일요일", "일요일")
        ],
        label="평일/주말"
    )

    # 시간대 선택 드롭다운 필드
    TIME_CHOICES = [
        (time, time) for time in DegreeOfSubwayCongestion.objects.values_list('time', flat=True).distinct()
    ]
    time = forms.ChoiceField(label='시간대 선택', choices=TIME_CHOICES)
    