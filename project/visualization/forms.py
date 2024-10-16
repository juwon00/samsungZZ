from django import forms

class StationSearchForm(forms.Form):
    station_name = forms.CharField(label='Station Name', max_length=100)
    line_number = forms.CharField(label='Line Number', max_length=20)