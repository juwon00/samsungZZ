from django import forms

#class StationSearchForm(forms.Form):
    

class SubwayDataForm(forms.Form):
    # line 필드는 드롭다운 형식
    LINE_CHOICES = [
        ('1호선', '1호선'),
        ('2호선', '2호선'),
        ('3호선', '3호선'),
        ('4호선', '4호선'),
        ('5호선', '5호선'),
        ('6호선', '6호선'),
        ('7호선', '7호선'),
        ('8호선', '8호선'),
    ]
    line = forms.ChoiceField(label='호선', choices=LINE_CHOICES)

    # 역이름은 문자열 입력
    sttn = forms.CharField(label='지하철역', max_length=20)

    #station_name = forms.CharField(label='Station Name', max_length=100)
    #line_number = forms.CharField(label='Line Number', max_length=20)