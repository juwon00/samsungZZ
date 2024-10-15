from rest_framework import serializers
from .models import SubwayMonthlyTimeSlotPassengerCounts


class SubwayPassengerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubwayMonthlyTimeSlotPassengerCounts
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("id", None)  # id 필드 제거
        return representation
