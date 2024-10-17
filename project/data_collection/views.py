from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubwayMonthlyTimeSlotPassengerCounts, DegreeOfSubwayCongestion, SubwayDailyTimeSlotPassengerDifference, SubwayAmenities
from .serializers import SubwayPassengerCountSerializer, DegreeOfSubwayCongestionSerializer, SubwayPassengerDifferenceSerializer, SubwayAmenitiesSerializer
import requests
import re
import folium

class SubwayMonthlyPassengerCounterListView(APIView):
    def get(self, request, *args, **kwargs):
        # 쿼리 파라미터에서 sttn과 line을 가져옴
        sttn = request.query_params.get("sttn", None)
        line = request.query_params.get("line", None)

        # 기본적으로 모든 데이터를 가져옴
        queryset = SubwayMonthlyTimeSlotPassengerCounts.objects.all()

        if sttn:
            queryset = queryset.filter(sttn=sttn)
        if line:
            queryset = queryset.filter(line=line)

        # Serializer로 데이터를 JSON 형식으로 직렬화
        serializer = SubwayPassengerCountSerializer(queryset, many=True)

        return Response(serializer.data[0])

class DegreeOfSubwayCongestionListView(APIView):
    def get(self, request, *args, **kwargs):
        week = request.query_params.get("week", None)
        route_name = request.query_params.get("route_name", None)
        time = request.query_params.get("time", None)

        queryset = DegreeOfSubwayCongestion.objects.all()

        if route_name:
            queryset = queryset.filter(route_name=route_name)
        if week:
            queryset = queryset.filter(week=week)
        if time:
            queryset = queryset.filter(time=time)
        
        serializer = DegreeOfSubwayCongestionSerializer(queryset, many=True)

        return Response(serializer.data)


class SubwayDailyPassengerDifferenceView(APIView):
    def get_coordinates_from_kakao(self, station_name):
        kakao_api_key = "280b770ef839100d3cfbd61f397633c9"  # Kakao REST API 키를 입력해야 합니다.
        station_name = re.sub(r"\([^)]*\)", "", station_name)
        # '역'이 없는 경우 추가: "강남" -> "강남역"
        if "서울역" not in station_name and not station_name.endswith("역"):
            station_name += "역"
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={station_name}"
        headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            documents = response.json().get("documents", [])
            if documents:
                longitude = float(documents[0]["x"])
                latitude = float(documents[0]["y"])
                return latitude, longitude
        return None, None 
    
    def create_default_map(self):
        #서울 중심을 기준으로 Folium 지도 초기화.
        return folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    
    def draw_passenger_difference(self, subway_map, station_name, difference, latitude, longitude):
        #승하차 인원 차이에 따라 CircleMarker를 Folium 지도에 추가.
        color = 'blue' if difference > 0 else 'red'
        folium.CircleMarker(
            location=[float(latitude), float(longitude)],
            radius=abs(difference) / 100,  # 차이에 비례한 원 크기
            popup=station_name,
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(subway_map)

    def get(self, request, date, line, sttn, time_slot):
        try:
            # 모든 역의 데이터를 가져옵니다.
            data_list = SubwayDailyTimeSlotPassengerDifference.objects.filter(
                date=date,
                line=line,
                # sttn=sttn,
                time_slot=time_slot
            )
            
            # 기본 지도 생성
            subway_map = self.create_default_map()
            
            for data in data_list:
                # Kakao API를 이용해 좌표 가져오기
                latitude, longitude = self.get_coordinates_from_kakao(data.sttn)
                
                if latitude and longitude:
                    # 데이터에 좌표 저장
                    data.latitude = latitude
                    data.longitude = longitude
                    data.save()

                    # 역별 인원 차이 데이터를 시각화
                    serializer = SubwayPassengerDifferenceSerializer(data)
                    self.draw_passenger_difference(
                        subway_map=subway_map,
                        station_name=serializer.data["sttn"],
                        difference=serializer.data["difference"],
                        latitude=serializer.data["latitude"],
                        longitude=serializer.data["longitude"]
                    )

            # Folium 지도를 HTML로 변환 후 렌더링
            map_html = subway_map._repr_html_()
            return render(request, "data_collection/map.html", {"map_html": map_html})

        except SubwayDailyTimeSlotPassengerDifference.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

class SubwayAmenitiesView(APIView):
    def get(self, request, line, sttn):
        try:
            data = SubwayAmenities.objects.get(
                line=line,
                sttn=sttn,
            )
            serializer = SubwayAmenitiesSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SubwayAmenities.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)