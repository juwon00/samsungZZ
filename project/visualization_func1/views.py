# Create your views here.

from django.shortcuts import render
from data_collection.models import DegreeOfSubwayCongestion
from .forms import congestionForm
import numpy as np
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 

def congestion_view(request):
    # initialize
    form = congestionForm()
    filtering_data = None
    grades = None
    result_data = []
    

    if request.method == 'POST':
        form = congestionForm(request.POST)
    
        if form.is_valid():

            route_name = form.cleaned_data['route_name']
            week = form.cleaned_data['week']
            time = form.cleaned_data['time']

            # 데이터 필터링
            filtering_data = DegreeOfSubwayCongestion.objects.filter(route_name=route_name, week=week, time=time)
            
            # 혼잡도 데이터를 리스트로 추출 
            congestion_list = [data.congestion for data in filtering_data]
            
            # 혼잡도의 평균과 표준편차 계산
            if congestion_list:
                avg_congestion = np.mean([c for c in congestion_list if c is not None]) # None 제외
                std_congestion = np.std([c for c in congestion_list if c is not None])  # None 제외
                
                
            # 평균과 표준편차를 사용해 혼잡도 등급 분류
                
            # 1~4로 혼잡한 정도 높아짐
            # 1. 평균 - 표준편차보다 작은 값
            # 2. 평균 - 표준편차 < data < 평균
            # 3. 평균 < data < 평균 + 표준편차
            # 4. 평균 + 표준편차보다 큰 값
                
            grades = []
            for congestion in congestion_list:
                if congestion is None: # 혼잡도가 None인 경우 등급도 None
                    grades.append(None)
                elif congestion < avg_congestion - std_congestion:
                    grades.append(1)
                elif avg_congestion - std_congestion <= congestion:
                    grades.append(2)
                elif avg_congestion <= congestion < avg_congestion + std_congestion:
                    grades.append(3)
                else:
                    grades.append(4)
        else:
            print("Form Errors: ", form.errors)
    
    # for data, grade in zip(filtering_data, grades):
        # 역 좌표 정보 가져오기
        # 데이터 병합 필요합니다.
        # station = Station.objects.get(name=data.station_name)
        # result_data.append((station, grade)) 
    
    # 필터링된 데이터와 혼잡도 등급을 연결
    if filtering_data and grades:
        for data, grade in zip(filtering_data, grades):
            # 필요한 필드를 추출하여 딕셔너리로 변환
            result_data.append({
                'sub_name' : data.sub_name,
                'route_name': data.route_name,
                'week': data.week,
                'time': data.time,
                'grade': grade,
            })
            
    context = {
        'form': form,
        # 필터링된 데이터와 혼잡도 등급 전달
        # 'result_data': result_data if filtering_data else None,
        'result_data': result_data
    }
    
    return render(request, 'congView.html', context)