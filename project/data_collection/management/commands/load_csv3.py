import pandas as pd
from django.core.management.base import BaseCommand
from data_collection.models import SubwayDailyTimeSlotPassengerDifference

class Command(BaseCommand):
    help = 'Load data from CSV file(data3) into the Subway Daily Time Slot Passenger Difference model'

    def handle(self, *arg, **kwargs):
        csv_file_path = 'Data3.csv'
        df = pd.read_csv(csv_file_path, encoding='cp949')
        l = len(df)
        self.stdout.write("Data reading complete")

        for i, row in df.iterrows():
            SubwayDailyTimeSlotPassengerDifference.objects.update_or_create(
                date=row['날짜'],
                line=row['호선'],
                sttn=row['역명'],
                time_slot=row['시간대'],
                defaults={'difference': row['승차_하차_차이']}
            )
            if i % 10000 == 0 or i == l:
                self.stdout.write(f"({i}/{l})")
        self.stdout.write(self.style.SUCCESS('Data loading complete'))