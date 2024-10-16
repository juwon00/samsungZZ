import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from .forms import SubwayDataForm
from data_collection.models import SubwayMonthlyTimeSlotPassengerCounts
import matplotlib.pyplot as plt

import numpy as np
import io, urllib, base64

def subway_passenger_graph(request):
    # 요청이 POST일 때 (사용자가 입력값 보냄)
    graph = None
    error_message = None
    if request.method == 'POST':
        form = SubwayDataForm(request.POST)

        if form.is_valid():
            line = form.cleaned_data['line']
            sttn = form.cleaned_data['sttn']

            # 검색한 노선과 역에 해당하는 데이터 조회
            data = SubwayMonthlyTimeSlotPassengerCounts.objects.filter(line=line, sttn=sttn)

            if data.exists(): # 데이터가 제대로 입력
                # 시간대 -> x축 라벨
                times = [f'{i}-{i+1}시' for i in range(4, 24)]
                # 시간대별 승차인원 데이터
                get_on = [getattr(data.first(), f'hr_{i}_get_on_nope')//30 for i in range(4, 24)]
                # 시간대별 하차인원 데이터
                get_off = [getattr(data.first(), f'hr_{i}_get_off_nope')//30 for i in range(4, 24)]
                
                # 한글 설정
                plt.rc('font', family='Malgun Gothic')
                plt.rcParams['axes.unicode_minus'] = False

                # 그래프 그리기
                fig, ax = plt.subplots(figsize=(12, 6))
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
                {'form': form, 'graph': graph, 'error_message':error_message})