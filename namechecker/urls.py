from django.conf.urls import url,include,patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.Index.as_view(), name='index'),
                       )