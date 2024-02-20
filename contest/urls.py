from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^contests/$', views.contests, name='contests'),
    re_path(r'^contest/(?P<contest_id>[0-9]+)/$', views.contest, name='contest'),  
    re_path(r'^contest/(?P<contest_id>[0-9]+)/submit/(?P<problem_id>[A-Z]+)/$', views.contest_submit, name='contest_submit'), 
    re_path(r'^contest/(?P<contest_id>[0-9]+)/problem/(?P<problem_id>[A-Z]+)/$', views.contest_problem, name='contest_problem'), 
    re_path(r'^contest/(?P<contest_id>[0-9]+)/status/$', views.contest_status, name='contest_status'),
    re_path(r'^code/(?P<submission_id>[0-9]+)/$', views.code, name='code'),
    re_path(r'^contest/(?P<contest_id>[0-9]+)/standings/$', views.contest_standings, name='contest_standings'),
]
