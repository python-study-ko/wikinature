from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.shortcuts import render
import os
from .forms import ImportFile
import tempfile
from .checker import Checker

def upload_check(file,rowname,rownum):
    """ 업로드 자료 무결성 검증 함수"""
    pass

class Index(View):
    def get(self, request, data=None):
        form = ImportFile()
        context = {'test':'filecheck','upload':'no', 'form':form}

        data = render_to_string('check/index.html',context,request=request)
        return HttpResponse(data)

    def post(self, request):
        """ 식물목록 엑셀파일, 시트명, 머리열 위치, 머리열 이름값을 전달 받아 결과를 처리"""
        # 할일: Form.errors 로 에러데이터를 프론트에 전달하도록 처리
        # 할일: 업로드 무결성 검사를 뷰로직에서 분리하여 처리하기
        form = ImportFile(request.POST,request.FILES)

        if form.is_valid(): # 파일이 업로드 되었을 경우
            # 업로드한 파일및 엑셀 속성값 호출
            file = request.FILES['file']    # 업로드된 파일
            sheet_name = request.POST['sheetname'] # 식물 목록이 존해하는 시트이름
            row_name = request.POST['rowname'] # 식물 목록의 머릿행 이름
            # 머릿행의 번호
            # 할일: 폼에서 필수 값으로 변경하고 단순대입 하도록 조정하기
            if request.POST['rownum']:
               row_num = int(request.POST['rownum'])-1
            else:
                row_num = 0

            # 파일 형식확인 : 엑셀파일이 아닐경우
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                upload = 'no'
                test = file.content_type
                message = '엑셀파일이 아닌거 같습니다. 파일 확장자를 확인해주시고 업로드 하세요'
            else:
                # 업로드 파일을 임시파일로 저장하기
                # tmp = tempfile.NamedTemporaryFile()
                # tmp.write(file.read())
                # 엑셀 파일을 불러 시트 목록 출력하기

                target = Checker()
                error_chekc = target.setdata(file,sheet_name,row_name,row_num)

                # 엑셀 작업을 위한 구조 파익에 실패할 경우
                if error_chekc:
                    upload = 'no'
                    message = '시트명,머리열 이름, 머리열 위치 를 다시 확인해 주시기 바랍니다. {}'.format(error_chekc)
                # 엑셀 매칭 작업
                else:
                    # 매칭 작업
                    target.search()
                    # 작업 완료된 파일 저장
                    file_name = '{} wikinature.xlsx'.format(datetime.now())
                    target.file.save(file_name)
                    # 작업 완료된 파일을 리스폰
                    try:
                        with open(file_name, 'rb') as f:
                            upload = 'yes'
                            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
                            response['Content-Disposition'] = 'attachment; filename="wikinature.xls"'
                            return response
                    finally:
                        # 작업 완료된 파일 삭제
                        os.remove(file_name)

        else:   # 업로드 파일이 없을 경우
            upload = 'no'
            message = '이런, 파일을 올리신게 맞나요? 저는 아무것도 받지 못했습니다.. 다시 확인해 주세요'

        # 작업 실패시 에러 메시지를 리스폰
        form = ImportFile()
        context = { 'upload': upload, 'message': message, 'form':form}
        data = render_to_string('check/index.html', context, request=request)
        return HttpResponse(data)