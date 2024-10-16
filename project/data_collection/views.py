from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubwayMonthlyTimeSlotPassengerCounts, SubwayDailyTimeSlotPassengerDifference, SubwayStationLatLng
from .serializers import SubwayPassengerCountSerializer, SubwayPassengerDifferenceSerializer, SubwayStationLatLngSerializer


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


class SubwayStationLatLngListView(APIView):
    def get(self, request, *args, **kwargs):
        route_name = request.query_params.get("route_name", None)

        queryset = SubwayStationLatLng.objects.all()

        if route_name:
            queryset = queryset.filter(route_name=route_name)

        serializer = SubwayStationLatLngSerializer(queryset, many=True)

        return Response(serializer.data)

      
class SubwayDailyPassengerDifferenceView(APIView):
    def get(self, request, date, line_number, station_name, time_slot):
        try:
            data = SubwayDailyTimeSlotPassengerDifference.objects.get(
                date=date,
                line_number=line_number,
                station_name=station_name,
                time_slot=time_slot
            )
            serializer = SubwayPassengerDifferenceSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SubwayDailyTimeSlotPassengerDifference.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
