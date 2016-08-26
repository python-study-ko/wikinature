from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.shortcuts import render
import os
from .forms import ImportFile
import tempfile
from .checker import Checker

class Index(View):
    def get(self, request, data=None):
        form = ImportFile()
        context = {'test':'filecheck','upload':'no', 'form':form}

        data = render_to_string('check/index.html',context,request=request)
        return HttpResponse(data)

    def post(self, request):
        form = ImportFile(request.POST,request.FILES)
        test = 'filecheck'
        if form.is_valid(): # 파일이 업로드 되었을 경우
            # 업로드한 파일및 엑셀 속성값 호출
            file = request.FILES['file']    # 업로드된 파일
            sheet_name = request.POST['sheetname'] # 식물 목록이 존해하는 시트이름
            row_name = request.POST['rowname'] # 식물 목록의 머릿행 이름
            # 머릿행의 번호
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
                try:
                    target = Checker()
                    target.setdata(file,sheet_name,row_name,row_num)
                    target.search()
                    file_name = '{} wikinature.xlsx'.format(datetime.now())
                    target.file.save(file_name)
                    try:
                        with open(file_name,'rb') as f:
                            upload = 'yes'
                            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
                            response['Content-Disposition'] = 'attachment; filename="wikinature.xls"'
                            return response
                    except:
                        pass

                    finally:
                        os.remove(file_name)


                except EOFError as e:
                    upload = 'no'
                    message = '지원하지 않는 엑셀 구조 입니다.관리자 에게 문의해 주세요  {}'.format(e)


        else:   # 업로드 파일이 없을 경우
            upload = 'no'
            message = '이런, 파일을 올리신게 맞나요? 저는 아무것도 받지 못했습니다.. 다시 확인해 주세요'
        form = ImportFile()
        context = {'test': test, 'upload': upload, 'message': message, 'form':form}
        data = render_to_string('check/index.html', context, request=request)
        return HttpResponse(data)