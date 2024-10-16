import requests
import json
from collections import Counter
from django.core.management.base import BaseCommand
from ...models import SubwayMonthlyTimeSlotPassengerCounts


class Command(BaseCommand):
    help = "Fetch subway data and store it in the database"

    def handle(self, *args, **kwargs):
        url = "http://openapi.seoul.go.kr:8088/46426367776a7577393951585a7847/json/CardSubwayTime/1/700/202409"
        response = requests.get(url)

        decoded_content = response.content.decode("utf-8")
        json_data = json.loads(decoded_content)

        valid_sbwy_rout_ln_nm = [
            "1호선",
            "2호선",
            "3호선",
            "4호선",
            "5호선",
            "6호선",
            "7호선",
            "8호선",
        ]
        trans_to_1_sbwy_rout_ln_nm = ["경원선", "경인선", "경부선", "장항선"]
        trans_to_3_sbwy_rout_ln_nm = ["일산선"]
        trans_to_4_sbwy_rout_ln_nm = ["과천선", "안산선"]

        rows = json_data["CardSubwayTime"]["row"]
        for row in rows:

            # trans_to_1,3,4_sbwy_rout_ln_nm 역들 각각 1호선, 3호선, 4호선으로 바꿈
            original_sbwy_rout_ln_nm = row["SBWY_ROUT_LN_NM"]

            if original_sbwy_rout_ln_nm in valid_sbwy_rout_ln_nm:
                sbwy_rout_ln_nm = original_sbwy_rout_ln_nm
            elif original_sbwy_rout_ln_nm in trans_to_1_sbwy_rout_ln_nm:
                sbwy_rout_ln_nm = "1호선"
                # 서울역, 청량리(서울시립대입구), 지축 3개의 역이 2번 집계됨 - 하나 건너뛰도록
                if row["STTN"] == "서울역" or row["STTN"] == "청량리(서울시립대입구)":
                    continue
            elif original_sbwy_rout_ln_nm in trans_to_3_sbwy_rout_ln_nm:
                sbwy_rout_ln_nm = "3호선"
                if row["STTN"] == "지축":
                    continue
            elif original_sbwy_rout_ln_nm in trans_to_4_sbwy_rout_ln_nm:
                sbwy_rout_ln_nm = "4호선"
            else:
                continue

            SubwayMonthlyTimeSlotPassengerCounts.objects.create(
                line=sbwy_rout_ln_nm,
                sttn=row["STTN"],
                hr_4_get_on_nope=row["HR_4_GET_ON_NOPE"],
                hr_4_get_off_nope=row["HR_4_GET_OFF_NOPE"],
                hr_5_get_on_nope=row["HR_5_GET_ON_NOPE"],
                hr_5_get_off_nope=row["HR_5_GET_OFF_NOPE"],
                hr_6_get_on_nope=row["HR_6_GET_ON_NOPE"],
                hr_6_get_off_nope=row["HR_6_GET_OFF_NOPE"],
                hr_7_get_on_nope=row["HR_7_GET_ON_NOPE"],
                hr_7_get_off_nope=row["HR_7_GET_OFF_NOPE"],
                hr_8_get_on_nope=row["HR_8_GET_ON_NOPE"],
                hr_8_get_off_nope=row["HR_8_GET_OFF_NOPE"],
                hr_9_get_on_nope=row["HR_9_GET_ON_NOPE"],
                hr_9_get_off_nope=row["HR_9_GET_OFF_NOPE"],
                hr_10_get_on_nope=row["HR_10_GET_ON_NOPE"],
                hr_10_get_off_nope=row["HR_10_GET_OFF_NOPE"],
                hr_11_get_on_nope=row["HR_11_GET_ON_NOPE"],
                hr_11_get_off_nope=row["HR_11_GET_OFF_NOPE"],
                hr_12_get_on_nope=row["HR_12_GET_ON_NOPE"],
                hr_12_get_off_nope=row["HR_12_GET_OFF_NOPE"],
                hr_13_get_on_nope=row["HR_13_GET_ON_NOPE"],
                hr_13_get_off_nope=row["HR_13_GET_OFF_NOPE"],
                hr_14_get_on_nope=row["HR_14_GET_ON_NOPE"],
                hr_14_get_off_nope=row["HR_14_GET_OFF_NOPE"],
                hr_15_get_on_nope=row["HR_15_GET_ON_NOPE"],
                hr_15_get_off_nope=row["HR_15_GET_OFF_NOPE"],
                hr_16_get_on_nope=row["HR_16_GET_ON_NOPE"],
                hr_16_get_off_nope=row["HR_16_GET_OFF_NOPE"],
                hr_17_get_on_nope=row["HR_17_GET_ON_NOPE"],
                hr_17_get_off_nope=row["HR_17_GET_OFF_NOPE"],
                hr_18_get_on_nope=row["HR_18_GET_ON_NOPE"],
                hr_18_get_off_nope=row["HR_18_GET_OFF_NOPE"],
                hr_19_get_on_nope=row["HR_19_GET_ON_NOPE"],
                hr_19_get_off_nope=row["HR_19_GET_OFF_NOPE"],
                hr_20_get_on_nope=row["HR_20_GET_ON_NOPE"],
                hr_20_get_off_nope=row["HR_20_GET_OFF_NOPE"],
                hr_21_get_on_nope=row["HR_21_GET_ON_NOPE"],
                hr_21_get_off_nope=row["HR_21_GET_OFF_NOPE"],
                hr_22_get_on_nope=row["HR_22_GET_ON_NOPE"],
                hr_22_get_off_nope=row["HR_22_GET_OFF_NOPE"],
                hr_23_get_on_nope=row["HR_23_GET_ON_NOPE"],
                hr_23_get_off_nope=row["HR_23_GET_OFF_NOPE"],
                hr_0_get_on_nope=row["HR_0_GET_ON_NOPE"],
                hr_0_get_off_nope=row["HR_0_GET_OFF_NOPE"],
                hr_1_get_on_nope=row["HR_1_GET_ON_NOPE"],
                hr_1_get_off_nope=row["HR_1_GET_OFF_NOPE"],
                hr_2_get_on_nope=row["HR_2_GET_ON_NOPE"],
                hr_2_get_off_nope=row["HR_2_GET_OFF_NOPE"],
                hr_3_get_on_nope=row["HR_3_GET_ON_NOPE"],
                hr_3_get_off_nope=row["HR_3_GET_OFF_NOPE"],
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully saved subway data to the database.")
        )
