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
            return HttpResponseRedirect('/success/url/')
        else:
            return HttpResponseRedirect('/fail/url')
        """
        context = {'test': file, 'upload':'yes'}
        data = render_to_string('check/index.html', context, request=request)
        return HttpResponse(data)
        """