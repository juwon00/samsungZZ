import pandas as pd
from django.core.management.base import BaseCommand
from data_collection.models import SubwayAmenities

class Command(BaseCommand):
    help = 'Load data from CSV file(data3) into the Subway Daily Time Slot Passenger Difference model'

    def handle(self, *arg, **kwargs):
        csv_file_path = '../project/data/Data4.csv' # data 폴더에 csv파일 추가하고 상대경로 입력
        df = pd.read_csv(csv_file_path, encoding='cp949')
        l = len(df)
        self.stdout.write("Data reading complete")

        for i, row in df.iterrows():
            SubwayAmenities.objects.update_or_create(
                line=row['호선'],
                sttn=row['역명'],
                
                culture_space=row['문화공간여부'],
                wheelchair_lift=row['휠체어리프트여부'],
                meeting_place=row['만남의장소여부'],
                transfer_parking_lot=row['환승주차장여부'],
                bicycle_storage=row['자전거보관소여부'],
                elevator=row['엘리베이터여부'],
                train_reservation=row['기차예매역여부'],
                civil_service_machine=row['무인민원발급기여부'],
                exchange_kiosk=row['환전키오스크여부'],
                nursing_room=row['수유실여부'],
            )
            if i % 100 == 0 or i == l:
                self.stdout.write(f"({i}/{l})")
        self.stdout.write(self.style.SUCCESS('Data loading complete'))