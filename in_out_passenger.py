import pandas as pd
import folium
import re
import requests

class SeoulSubway:
    def __init__(self, csv_path, kakao_api_key):
        self.df = pd.read_csv(csv_path, encoding='cp949')
        self.headers = {'Authorization': f'KakaoAK {kakao_api_key}'}
        self.result = None
        self.station_map_dict = {}
    
    def preprocess_data(self):
        # 날짜 형식 변환 및 5월 데이터 필터링(10/15 회의 결정사항)
        self.df['날짜'] = pd.to_datetime(self.df['날짜'], errors='coerce')
        self.df = self.df[(self.df['날짜'].dt.year == 2024) & (self.df['날짜'].dt.month == 5)].reset_index()

        # 역명 전처리
        self.df['역명'] = self.df['역명'].apply(lambda x: re.sub(r'\([^)]*\)', '', x) if '(' in x else x)
        self.df['역명'] = self.df['역명'].apply(lambda x: x + '역' if '서울역' not in x else x)

    def fetch_coordinates(self):
        # 카카오 API: 각 역의 좌표 가져오기
        distinct_station_names = self.df['역명'].unique()
        x, y = [], []

        for name in distinct_station_names:
            url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={name}'
            places = requests.get(url, headers=self.headers).json()['documents'][0]
            x.append(places['y'])
            y.append(places['x'])

        self.station_map_dict = {name: [x[i], y[i]] for i, name in enumerate(distinct_station_names)}

    def map_coordinates(self):
        # df에 좌표 매핑
        for i in range(len(self.df)):
            station = self.df.loc[i, '역명']
            self.df.at[i, 'latitude'] = self.station_map_dict[station][0]
            self.df.at[i, 'longitude'] = self.station_map_dict[station][1]

    def generate_pivot(self):
        # 시간대 열 정의 및 피벗 테이블 생성
        time_cols = [
            '06시 이전', '06시-07시', '07시-08시', '08시-09시', '09시-10시',
            '10시-11시', '11시-12시', '12시-13시', '13시-14시', '14시-15시',
            '15시-16시', '16시-17시', '17시-18시', '18시-19시', '19시-20시',
            '20시-21시', '21시-22시', '22시-23시', '23시-24시', '24시 이후'
        ]

        pivot = self.df.pivot_table(
            index=['날짜', '호선', '역명', 'latitude', 'longitude'],
            columns='구분',
            values=time_cols,
            aggfunc='sum',
            fill_value=0
        )

        diff = pivot.xs('승차', level=1, axis=1) - pivot.xs('하차', level=1, axis=1)
        self.result = diff.reset_index().melt(
            id_vars=['날짜', '호선', '역명', 'latitude', 'longitude'],
            var_name='시간대', value_name='승차_하차_차이'
        )
        self.result['latitude'] = pd.to_numeric(self.result['latitude'], errors='coerce')
        self.result['longitude'] = pd.to_numeric(self.result['longitude'], errors='coerce')
        self.result['승차_하차_차이'] = self.result['승차_하차_차이'].astype(int)

    def visualize(self, date, line, time):
        # 필터링된 데이터로 지도 시각화
        table = self.result[
            (self.result['날짜'] == date) &
            (self.result['호선'] == line) &
            (self.result['시간대'] == time)
        ]

        map_ = folium.Map(location=[table['latitude'].mean(), table['longitude'].mean()], zoom_start=13)

        for _, row in table.iterrows():
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=abs(row['승차_하차_차이']) / 100,
                popup=row['역명'],
                color='blue' if row['승차_하차_차이'] > 0 else 'red',
                fill=True,
                fill_opacity=0.7
            ).add_to(map_)

        return map_

if __name__ == '__main__':
    kakao_api_key = 'TYPE_YOUR_KAKAO_API_AUTH'
    subway = SeoulSubway('서울교통공사_역별 일별 시간대별 승하차인원(24.2~24.5).csv', kakao_api_key)

    subway.preprocess_data()
    subway.fetch_coordinates()
    subway.map_coordinates()
    subway.generate_pivot()
    #날짜, 호선, 시간 -> input으로 들어가면
    map_ = subway.visualize('2024-05-01', '1호선', '07시-08시')
    # 해당 html이 output으로 나옴.
    map_.save('output.html')
