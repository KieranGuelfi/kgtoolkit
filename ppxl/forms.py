from socket import fromshare
from django import forms


class UploadReportForm(forms.Form):
    report = forms.FileField()
