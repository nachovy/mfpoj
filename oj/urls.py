from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^problemset/$', views.problemset, name='problemset'), 
    url(r'^problem/(?P<problem_id>[0-9]+)/$', views.problem, name='problem'), 
    url(r'^$', views.index, name='index'), 
]
