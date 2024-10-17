# Create your views here.

from django.shortcuts import render
from .models import DegreeOfSubwayCongestion
from .forms import FilterForm
import numpy as np

def congestion_view(request):
    # initialize
    form = FilterForm()
    filtering_data = None
    grades = None

    if request.method == 'POST':
        form = FilterForm(request.POST)
        
        if form.is_valid():
            route_name = form.cleaned_data['route_name']
            weekday_choice = form.cleaned_data['weekday']
            time = form.cleaned_data['time']
    
    # 평일/주말 데이터 치환
    # day = True, week = False
    weekday = True if weekday_choice == '1' else False

    # 데이터 필터링
    filtering_data = DegreeOfSubwayCongestion.objects.filter(route_name=route_name, weekday=weekday, time=time)

    # 혼잡도 데이터를 리스트로 추출
    congestion_list = [data.congestion for data in filtering_data]
    
    # 혼잡도의 평균과 표준편차 계산
    if congestion_list:
        avg_congestion = np.mean(congestion_list)   # 평균
        std_congestion = np.std(congestion_list)    # 표준편차
    
    
    # 평균과 표준편차를 사용해 혼잡도 등급 분류
    
    # 1~4로 혼잡한 정도 높아짐
    # 1. 평균 - 표준편차보다 작은 값
    # 2. 평균 - 표준편차 < data < 평균
    # 3. 평균 < data < 평균 + 표준편차
    # 4. 평균 + 표준편차보다 큰 값
    
    grades = []
    for congestion in congestion_list:
        if congestion < avg_congestion - std_congestion:
            grade = 1
        elif avg_congestion - std_congestion <= congestion:
            grade = 2
        elif avg_congestion <= congestion < avg_congestion + std_congestion:
            grade = 3
        else:
            grade = 4
        grades.append(grade)
        
    context = {
        'form': form,
        # 필터링한 데이터와 grades를 함께 묶어서 템플릿에 전달
        'result_data': zip(filtering_data, grades) if filtering_data else None,
    }
    
    return render(request, 'congestion.html', context)