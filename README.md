# samsungZZ

### csv 파일 다루기
#### 로드
1. `data_collection/manage/load_csv.py`에서 로드하고 싶은 csv 파일 경로 입력
2. 터미널에서 다음을 실행 `python manage.py load_csv`
#### 초기화
1. 터미널에서 shell을 열어서 사용
2. 다음을 입력하고 실행 `{모델}.objects.all().delete()`

### 지하철 역별 승하차인원 및 편의시설 정보 확인

1. (DB 실행) 터미널에서 다음을 실행 
* `python manage.py load_csv`
* `python manage.py fetch_subway_data`
2. (서버 접속) 터미널에서 서버 실행
* `python manage.py runserver`
* http://127.0.0.1:8000/subway/station-information 으로 접속
* 예시 화면
![스크린샷 2024-10-21 222927](https://github.com/user-attachments/assets/6e7b8ae3-2bc4-4eb2-9268-8cce9751c99d)


   
