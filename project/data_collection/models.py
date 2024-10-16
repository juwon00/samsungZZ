from django.db import models


class SubwayMonthlyTimeSlotPassengerCounts(models.Model):
    line = models.CharField(max_length=10)
    sttn = models.CharField(max_length=20)
    hr_4_get_on_nope = models.FloatField()
    hr_4_get_off_nope = models.FloatField()
    hr_5_get_on_nope = models.FloatField()
    hr_5_get_off_nope = models.FloatField()
    hr_6_get_on_nope = models.FloatField()
    hr_6_get_off_nope = models.FloatField()
    hr_7_get_on_nope = models.FloatField()
    hr_7_get_off_nope = models.FloatField()
    hr_8_get_on_nope = models.FloatField()
    hr_8_get_off_nope = models.FloatField()
    hr_9_get_on_nope = models.FloatField()
    hr_9_get_off_nope = models.FloatField()
    hr_10_get_on_nope = models.FloatField()
    hr_10_get_off_nope = models.FloatField()
    hr_11_get_on_nope = models.FloatField()
    hr_11_get_off_nope = models.FloatField()
    hr_12_get_on_nope = models.FloatField()
    hr_12_get_off_nope = models.FloatField()
    hr_13_get_on_nope = models.FloatField()
    hr_13_get_off_nope = models.FloatField()
    hr_14_get_on_nope = models.FloatField()
    hr_14_get_off_nope = models.FloatField()
    hr_15_get_on_nope = models.FloatField()
    hr_15_get_off_nope = models.FloatField()
    hr_16_get_on_nope = models.FloatField()
    hr_16_get_off_nope = models.FloatField()
    hr_17_get_on_nope = models.FloatField()
    hr_17_get_off_nope = models.FloatField()
    hr_18_get_on_nope = models.FloatField()
    hr_18_get_off_nope = models.FloatField()
    hr_19_get_on_nope = models.FloatField()
    hr_19_get_off_nope = models.FloatField()
    hr_20_get_on_nope = models.FloatField()
    hr_20_get_off_nope = models.FloatField()
    hr_21_get_on_nope = models.FloatField()
    hr_21_get_off_nope = models.FloatField()
    hr_22_get_on_nope = models.FloatField()
    hr_22_get_off_nope = models.FloatField()
    hr_23_get_on_nope = models.FloatField()
    hr_23_get_off_nope = models.FloatField()
    hr_0_get_on_nope = models.FloatField()
    hr_0_get_off_nope = models.FloatField()
    hr_1_get_on_nope = models.FloatField()
    hr_1_get_off_nope = models.FloatField()
    hr_2_get_on_nope = models.FloatField()
    hr_2_get_off_nope = models.FloatField()
    hr_3_get_on_nope = models.FloatField()
    hr_3_get_off_nope = models.FloatField()

    class Meta:
        db_table = "subway_monthly_time_slot_passenger_counts"

class SubwayDailyTimeSlotPassengerDifference(models.Model):
    date = models.DateField() 
    line_number = models.CharField(max_length=10)
    station_name = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=20)
    difference = models.IntegerField()

    class Meta:
        db_table = "subway_daily_time_slot_passenger_difference"

class SubwayAmenities(models.Model):
    line_number = models.CharField(max_length=10)
    station_name = models.CharField(max_length=20)
    
    culture_space = models.CharField(max_length=2)
    wheelchair_lift = models.CharField(max_length=2)
    meeting_place = models.CharField(max_length=2)
    transfer_parking_lot = models.CharField(max_length=2)
    bicycle_storage = models.CharField(max_length=2)
    elevator = models.CharField(max_length=2)
    train_reservation = models.CharField(max_length=2)
    civil_service_machine = models.CharField(max_length=2)
    exchange_kiosk = models.CharField(max_length=2)
    nursing_room = models.CharField(max_length=2)

    class Meta:
        db_table = "subway_amenities"