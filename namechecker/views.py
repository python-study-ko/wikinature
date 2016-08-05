from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import ImportFile



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
            # 업로드한 파일 호출
            file = request.FILES['file']

            # 파일 형식확인 : 엑셀파일이 아닐경우
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                upload = 'no'
                test = file.content_type
                message = '엑셀파일이 아닌거 같습니다. 파일 확장자를 확인해주시고 업로드 하세요'
            else:
                upload = 'yes'
                test = file.content_type
                message = '파일이 성공적으로 업로드 되었습니다. 잠시만 기다리시면 작업이 완료된 파일을 다운 받을수 있습니다.'

        else:   # 업로드 파일이 없을 경우
            upload = 'no'
            message = '이런, 파일을 올리신게 맞나요? 저는 아무것도 받지 못했습니다.. 다시 확인해 주세'
        form = ImportFile()
        context = {'test': test, 'upload': upload, 'message': message, 'form':form}
        data = render_to_string('check/index.html', context, request=request)
        return HttpResponse(data)