from django import forms

class ImportFile(forms.Form):
    file = forms.FileField(label='파일 선택하기', help_text='식물명을 찾을 파일을 업로드 하세')
    sheetname = forms.CharField(max_length=20,label='시트 이름', help_text='식물 목록이 있는 시트명을 입력하세요')
    rowname = forms.CharField(max_length=20,label='머리열 이름',help_text='식물 목록이 있는 열의 머리글 이름을 입력하세')
    rownum = forms.IntegerField(max_value=4,label='머리열 번호',help_text='시트의 첫번째 열이 머리열이 아닌경우 머리열 번호를 입력하세요', required=False)