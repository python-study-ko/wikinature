from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.
class Index(View):
    def get(self, request, data=None):

        context = {'test':'filecheck'}

        data = render_to_string('check/index.html',context,request=request)
        return HttpResponse(data)