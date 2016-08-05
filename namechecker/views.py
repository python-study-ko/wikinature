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
        if form.is_valid():
            # 업로드한 파일 호출
            file = request.FILES['file']

            # 파일 검사
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                return HttpResponseRedirect('/check/')

            context = {'test': file.content_type, 'upload': 'yes'}
            data = render_to_string('check/index.html', context, request=request)
            return HttpResponse(data)
        else:
            return HttpResponseRedirect('/check/')
