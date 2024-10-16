from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubwayMonthlyTimeSlotPassengerCounts
from .serializers import SubwayPassengerCountSerializer


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
