from django.core.management.base import BaseCommand
from ...PointScraper import PointScraper
import sqlite3
from ...models import SubwayStationLatLng


class Command(BaseCommand):
    help = "Subway latitude and longitude data fetcher"

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
        scraper = PointScraper()
        scraper.search(names)

        for station_name, (latitude, longitude) in scraper.result.items():
            route_name = station_name.split()[0]
            name = " ".join(station_name.split()[1:])

            station = SubwayStationLatLng(
                route_name=route_name, name=name, latitude=latitude, longitude=longitude
            )
            station.save()

        print("Data saved to the database.")
        print(scraper.result)
        print(scraper.not_found)
