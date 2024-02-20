from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^problemset/$', views.problemset, name='problemset'), 
    re_path(r'^problem/(?P<problem_id>[0-9]+)/$', views.problem, name='problem'),
    re_path(r'^user/(?P<user_id>[\s|\S]+)/$', views.user, name='user'), 
    re_path(r'^submit/(?P<problem_id>[0-9]+)/$', views.submit, name='submit'),
    re_path(r'^submit/$', views.submit, name='submit'),
    re_path(r'^code/(?P<submission_id>[0-9]+)/$', views.code, name='code'),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login/$', views.login, name='login'), 
    re_path(r'^register/$', views.register, name='register'), 
    re_path(r'^status/$', views.status, name='status'), 
    re_path(r'^ranklist/$', views.ranklist, name='ranklist'), 
    re_path(r'^modify/$', views.modify, name='modify'), 
    re_path(r'^logout/$', views.logout, name='logout'), 
]
