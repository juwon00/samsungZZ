from django import forms
from data_collection.models import DegreeOfSubwayCongestion

# 드롭다운 필드 정의
class FilterForm(forms.Form):
    route_choices = DegreeOfSubwayCongestion.objects.values_list('route_name', flat=True).distinct()
    time_choices = DegreeOfSubwayCongestion.objects.values_list('time', flat=True).distinct()

    route_name = forms.ChoiceField(choices=[(route, route) for route in route_choices], label="호선 선택")
    week = forms.ChoiceField(choices=[(1, "평일"), (2, "주말")], label="평일/주말")
    time = forms.ChoiceField(choices=[(time, time) for time in time_choices], label="시간대 선택")