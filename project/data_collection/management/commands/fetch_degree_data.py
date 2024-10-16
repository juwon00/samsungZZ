import requests
import json
from django.core.management.base import BaseCommand
import re

class Command(BaseCommand):
    help = "fetch the degree of subway congestion data and store it in the database"

    def handle(self, *args, **options):
        # Open API를 통해 데이터를 가져오기
        base_url = "https://api.odcloud.kr/api"
        endpoint = "/15071311/v1/uddi:9aff0ee6-26e7-42c4-af0c-84bf31680ca9"
        service_key = "CuIIBVTCl/wQJxJq6dTiCIpMsZCa2WddvKbBz+ocgbXi8m7aWKq0hfXyPI9raD98lb0d4yatCdoLr7Ad1LG4mQ=="
        url = f'{base_url}{endpoint}'
        params = {
            "serviceKey": service_key,
            "page": 1,
            "perPage": 100
        }

        data = []

        while True:
            response = requests.get(f"{base_url}{endpoint}", params=params)
            response_data = response.json()
            
            # 현재 페이지의 데이터를 가져옴
            current_data = response_data.get("data", [])
            data.extend(current_data)  # 모든 데이터를 저장할 리스트에 추가
            
            # 다음 페이지로 이동 (만약 현재 페이지에 데이터가 없으면 중단)
            if len(current_data) == 0:
                break
            
            params["page"] += 1  # 다음 페이지로 넘어감
        
        # 데이터 전처리: key값을 '00시 00분'에서 '00:00'으로 변경
        new_data = []
        new_dict = {}

        for item in data:
            for k, v in item.items():
                # '(0)0시 00분' 형태의 key값을 '00:00'으로 변경
                match = re.match(r'(\d{1,2})시(\d{2})분', k)
                # key값이 '0시 00분' 형태일 때
                if match and len(match.group(1)) == 1:
                    new_dict[('0' + match.group(1) + ':' + match.group(2))] = v
                # key값이 '00시 00분' 형태일 때
                elif match and len(match.group(1)) == 2:
                    new_dict[(match.group(1) + ":" + match.group(2))] = v
                # '(0)0시 00분' 형태가 아닌 모든 key값은 그대로 유지
                else:
                    new_dict[k] = v
            new_data.append(new_dict)
            new_dict = {}

        # 메모리 관리
        del(data, new_dict)

        print(new_data[:5])
