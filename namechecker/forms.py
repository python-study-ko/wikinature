from django import forms

class ImportFile(forms.Form):
    file = forms.FileField(label='파일 선택하기', help_text='식물명을 찾을 파일을 업로드 하세')