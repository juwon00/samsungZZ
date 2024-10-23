import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from data_collection.models import SubwayMonthlyTimeSlotPassengerCounts, SubwayAmenities
from .forms import SubwayDataForm
import matplotlib.pyplot as plt
import io
import urllib, base64
import matplotlib.font_manager as fm
import numpy as np


def subway_passenger_graph(request):
    graph = None
    error_message = None
    station = None
    max_get_on_count = '-'
    max_get_on_time = '-'
    max_get_off_count = '-'
    max_get_off_time = '-'
    if request.method == 'POST':
        form = SubwayDataForm(request.POST)
        if form.is_valid():
            line = form.cleaned_data['line'] # 'line' SubwayDataForm 클래스 안에 line 필드 정의
            sttn = form.cleaned_data['sttn']

            data = SubwayMonthlyTimeSlotPassengerCounts.objects.filter(line=line, sttn=sttn)
            station = SubwayAmenities.objects.filter(line=line, sttn=sttn).first()

            if data.exists():
                # 시간대, x축 라벨
                times = [f'{i}-{i+1}시' for i in range(4, 24)]
                # 시간대별 승차인원 데이터
                get_on = [getattr(data.first(), f'hr_{i}_get_on_nope')//30 for i in range(4, 24)]
                # 시간대별 하차인원 데이터
                get_off = [getattr(data.first(), f'hr_{i}_get_off_nope')//30 for i in range(4, 24)]
                
                # 최대 승차 인원 시간대 및 인원수
                max_get_on_count = int(max(get_on))
                max_get_on_time = times[get_on.index(max_get_on_count)]

                # 최대 하차 인원 시간대 및 인원수
                max_get_off_count = int(max(get_off))
                max_get_off_time = times[get_off.index(max_get_off_count)]

                # 한글 설정
                plt.rc('font', family='Malgun Gothic')
                plt.rcParams['axes.unicode_minus'] = False
                # 그래프 그리기
                fig, ax = plt.subplots(figsize=(8, 4))
                width = 0.35
                x = np.arange(len(times))

                ax.bar(x - width/2, get_on, width, label='승차인원', color='blue')
                ax.bar(x + width/2, get_off, width, label='하차인원', color='orange')

                ax.set_title(f'{line} {sttn}의 시간대별 승하차 인원수 (일별 추정치)')
                ax.set_xlabel('시간대')
                ax.set_ylabel('인원 수')
                ax.set_xticks(x)
                ax.set_xticklabels(times, rotation=45, ha='right')
                ax.legend()

                plt.tight_layout()
                plt.legend()

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                uri = 'data:image/png;base64,' + urllib.parse.quote(string)
                graph = uri
                plt.close()  # 그래프를 메모리에서 닫기
                
            else:
                error_message = "입력이 잘못되었습니다."
            
    else:
        form = SubwayDataForm()

    return render(request, 'subway_passenger_graph.html', 
                {'form': form, 'graph': graph, 'error_message':error_message, 'station':station, 
                'max_get_on_count': max_get_on_count, 'max_get_on_time': max_get_on_time,
                'max_get_off_count': max_get_off_count, 'max_get_off_time': max_get_off_time})