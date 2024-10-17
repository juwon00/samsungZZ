from django.core.management.base import BaseCommand
import sqlite3
from ...models import SubwayStationLatLng
import requests


class Command(BaseCommand):
    help = "Subway latitude and longitude data fetcher"

    def get_lat_lon(self, addr):
        api_key = "4408c2262908b5c0a96f61beee8e80f2"
        headers = {"Authorization": f"KakaoAK {api_key}"}  # REST API 키(유효한 키)
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={addr}"
        result = requests.get(url, headers=headers).json()
        print("result")
        print(result)

        lat = float(result["documents"][0]["y"])
        lon = float(result["documents"][0]["x"])

        return lat, lon

    def get_names_from_db(self):
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT line, sttn FROM subway_monthly_time_slot_passenger_counts"
        )
        rows = cursor.fetchall()
        names = [f"{line} {sttn}" for line, sttn in rows]
        connection.close()
        return names

    def handle(self, *args, **kwargs):
        print("Fetching subway latitude and longitude data...")
        names = self.get_names_from_db()  # DB에서 names 가져오기
        print(names)

        for name in names:
            print()
            line, sttn = name.split()
            index = name.find("(")
            if index != -1:
                name = name[:index]
            print(name)
            lat, lon = self.get_lat_lon(name)
            print(f"lat: {lat}, lon: {lon}")

            station = SubwayStationLatLng(
                route_name=line, name=sttn, latitude=lat, longitude=lon
            )
            station.save()

        # for station_name, (latitude, longitude) in scraper.result.items():
        #    route_name = station_name.split()[0]
        #    name = " ".join(station_name.split()[1:])

        #    station = SubwayStationLatLng(
        #        route_name=route_name, name=name, latitude=latitude, longitude=longitude
        #    )
        #    station.save()

        # print("Data saved to the database.")
        # print(scraper.result)
        # print(scraper.not_found)
