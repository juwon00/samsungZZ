from django.shortcuts import render
from .models import Amenities
from .forms import StationSearchForm

def station_search(request):
    if request.method == 'POST':
        form = StationSearchForm(request.POST)
        if form.is_valid():
            station_name = form.cleaned_data['station_name']
            line_number = form.cleaned_data['line_number']
            # 데이터베이스에서 해당 역과 호선이 일치하는 데이터를 검색
            station = Amenities.objects.filter(station_name=station_name, line_number=line_number).first()
            return render(request, 'amenities_result.html', {'station': station})
    else:
        form = StationSearchForm()

    return render(request, 'station_search.html', {'form': form})