import json
import time
import hashlib

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Problem, Submission, Waiting, User
from contest.models import Contest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    if('username' in request.session.keys()):
        s = User.objects.filter(username=request.session['username'])[0]
        obj = json.loads(s.ips)
        obj.append(ip)
        s.ips = json.dumps(obj)
        s.save()
        
        context = {'ip': ip, 'logined': 1, 'name': request.session['username']}
    else:
        context = {'ip': ip, 'logined': 0, 'name': ''}
    return render(request, 'index.html',context)
   # return HttpResponse("欢迎来到魔法炮OJ！")

def problemset(request):
    problem_list = Problem.objects.all()
    
    problems_per_page = 20 
    paginator = Paginator(problem_list, problems_per_page)
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    page_l = int(nowpage) - 2
    page_r = int(nowpage) + 2
    try:
        problem_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        problem_list = paginator.page(1)
    except EmptyPage:
        problem_list = paginator.page(paginator.num_pages)
   
    
    if('username' in request.session.keys()):
        s = User.objects.filter(username=request.session['username'])[0]
        obj = json.loads(s.stat)
        root = s.root
        context = {'page_l':page_l, 'page_r':page_r, 'stat': obj,'problem_list': problem_list,'logined': 1, 'root': root, 'name': request.session['username']}
    else:
        context = {'page_l':page_l, 'page_r':page_r, 'problem_list': problem_list,'logined': 0, 'root': 0, 'name': ''}
    return render(request, 'problemset.html', context)

def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    if('username' in request.session.keys()):
        root = User.objects.filter(username=request.session['username'])[0].root
        context = {'problem': problem,'logined': 1, 'root': root, 'name': request.session['username']}
    else:
        context = {'problem': problem,'logined': 0, 'root': 0, 'name': ''}
    return render(request, 'problem.html', context)

def user(request, user_id):
    user = User.objects.filter(username=user_id)[0]
    if('username' in request.session.keys()):
        context = {'user': user,'logined': 1, 'name': request.session['username']}
    else:
        context = {'user': user,'logined': 0, 'name': ''}
    return render(request, 'user.html', context)
    
def code(request, submission_id):
    user = User.objects.filter(username=request.session['username'])[0]
    submission = Submission.objects.get(pk=submission_id)
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))
    if('username' in request.session.keys()):
        context = {'user': user, 'nowtime': nowtime, 'submission': submission,'logined': 1, 'name': request.session['username']}
    else:
        context = {'user': user, 'nowtime': nowtime, 'submission': submission,'logined': 0, 'name': ''}
    return render(request, 'code.html', context)

def submit(request, **kwargs):
    if request.method == 'POST':
        if 'username' in request.session.keys():
            running = 0
            for contest in Contest.objects.all():
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8)) >= contest.start.strftime('%Y-%m-%d %H:%M:%S') and time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8)) <= contest.end.strftime('%Y-%m-%d %H:%M:%S'):
                    running = 1
            if Problem.objects.get(pk=request.POST['problem_id']).hide == 1:
                running = 2
            if running == 0 or User.objects.filter(username=request.session['username'])[0].root == 1:
                submission = Submission(
                                 problem=Problem.objects.get(pk=request.POST['problem_id']),
                                 source=request.POST['source'],
                                 language=request.POST['language'],
                                 user=User.objects.filter(username=request.session['username'])[0],
                                 length=len(request.POST['source']),
                                 submit_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8)),
                                 status="Pending", 
                                 score=0,
                                 time_used=0, 
                                 memory_used=0,
                             )
                submission.save()
                waiting=Waiting(submission=submission)
                waiting.save()
                
                s = User.objects.filter(username=request.session['username'])[0]
                s.submit += 1
                s.save()
                
                p = Problem.objects.get(pk=request.POST['problem_id'])
                p.submit += 1
                p.save()
                
                obj = json.loads(s.stat)
                if '%d'%p.id in obj.keys():
                    pass
                else:
                    obj['%d'%p.id] = 0
                    s.stat = json.dumps(obj)
                    s.save()
                    
                return HttpResponseRedirect('/status')
            elif running == 1:
                return HttpResponse("There is a contest running.")
            elif running == 2:
                return HttpResponse("You can't submit to this problem.")
        else:
            return HttpResponse("You should login first.")
    if 'problem_id' in kwargs.keys():
        problem = Problem.objects.get(pk=kwargs['problem_id'])
    else:
        problem = None
    
    if('username' in request.session.keys()):
        context = {'problem': problem,'logined': 1, 'name': request.session['username']}
    else:
        context = {'problem': problem,'logined': 0, 'name': ''}
    return render(request, 'submit.html', context)

def password_md5(password):
    return hashlib.md5(password.encode()).hexdigest()
    
def login(request):
    error_message = ""
    if request.method == 'POST':
        if len(request.POST['username']) == 0:
            error_message = "Empty username."
        elif len(request.POST['password']) == 0:
            error_message = "Empty password."
        else:
            s = User.objects.filter(username=request.POST['username'])
            if len(s) == 0 or password_md5(request.POST['password']) != s[0].password:
                error_message = "Incorrect username or password."
            else:
                request.session['username'] = request.POST['username']
                return HttpResponseRedirect('/')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'logined': 0, 'name': ''}
    return render(request, 'login.html', context)

def check_string_valid(String):
    for single_char in String:
        if single_char.isdigit() == 0 and single_char.isalpha() == 0 and single_char != '_' :
            return 0
    return 1

def register(request):
    def stat_default():
        return {"Accepted": 0, 
                "Presentation Error": 0, 
                "Time Limit Exceeded": 0, 
                "Memory Limit Exceeded": 0, 
                "Wrong Answer": 0, 
                "Runtime Error": 0, 
                "Output Limit Exceeded": 0, 
                "Compile Error": 0, 
                "System Error": 0, 
               }

    error_message = ""
    if request.method == 'POST':
        if request.POST['password'] != request.POST['password2']:
            error_message = "Passwords mismatched."
        elif len(request.POST["username"]) == 0:
            error_message = "Empty username."
        elif len(request.POST["username"]) > 15:
            error_message = "Username too long."
        elif len(request.POST["password"]) == 0:
            error_message = "Empty password."
        elif len(request.POST["password"]) > 20:
            error_message = "Password too long."
        elif check_string_valid(request.POST["username"]) == 0:
            error_message = "Invalid username."
        elif check_string_valid(request.POST["password"]) == 0:
            error_message = "Invalid password."
        elif len(User.objects.filter(username=request.POST['username'])):
            error_message = "This username has been registered."
        else:
            user = User(username=request.POST['username'], 
                        password=password_md5(request.POST['password']),
                        nickname=request.POST['username'], 
                        stat=json.dumps(stat_default()))
            user.submit = 0
            user.ac = 0
            user.save()
            return HttpResponseRedirect('/login')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        context = {'error_message': error_message,'logined': 0, 'name': ''}
    return render(request, 'register.html', context)

def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/')

def ranklist(request):
    all_user_list = User.objects.order_by("-ac","submit","username")
    user_list = User.objects.order_by("-ac","submit","username")
    # Paginator begins
    users_per_page = 50
    paginator = Paginator(user_list, users_per_page)
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    page_l = int(nowpage) - 2
    page_r = int(nowpage) + 2
    try:
        user_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    # Paginator ends
    if('username' in request.session.keys()):
        context = {'page_l':page_l, 'page_r':page_r, 'all_user_list':all_user_list,'user_list':user_list,'logined': 1, 'name': request.session['username']}
    else:
        context = {'page_l':page_l, 'page_r':page_r, 'all_user_list':all_user_list,'user_list':user_list,'logined': 0, 'name': ''}
    return render(request, 'ranklist.html',context)

def status(request):
    submission_list = Submission.objects.all()
    submission_list = list(submission_list)
    submission_list.reverse()
    
    for submission in submission_list:
        if submission.from_contest != 0:
            contest = Contest.objects.get(pk=submission.from_contest)
            submission.contest_start_time = contest.start
            submission.contest_end_time = contest.end
    # Paginator begins
    if 'page' in request.GET.keys():
        nowpage = request.GET['page']
    else:
        nowpage = 1
    submissions_per_page = 10
    paginator = Paginator(submission_list, submissions_per_page)
    page_l = int(nowpage) - 2
    page_r = int(nowpage) + 2
    try:
        submission_list = paginator.page(nowpage) 
    except PageNotAnInteger:
        submission_list = paginator.page(1)
    except EmptyPage:
        submission_list = paginator.page(paginator.num_pages)
    # Paginator ends
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8))
    if('username' in request.session.keys()):
        user = User.objects.filter(username=request.session['username'])[0]
        context = {'page_l':page_l, 'page_r':page_r, 'nowtime': nowtime, 'submission_list': submission_list,'logined': 1, 'root': user.root, 'name': request.session['username']}
    else:
        context = {'page_l':page_l, 'page_r':page_r, 'nowtime': nowtime, 'submission_list': submission_list,'logined': 0, 'root': 0,	'name': ''}
    return render(request, 'status.html',context)

def modify(request):
    error_message = ""
    if request.method == 'POST':
        if len(request.POST['opassword']) == 0:
            error_message = "Please input old password."
        else:
            s = User.objects.filter(username=request.session['username'])[0]
            if password_md5(request.POST['opassword']) != s.password:
                error_message = "Incorrect old password."
            elif request.POST['password'] != request.POST['password2']:
                error_message = "Passwords mismatched."
            elif len(request.POST["password"]) > 20:
                error_message = "Password too long."
            else:
                if len(request.POST['nickname']) != 0:
                    s.nickname=request.POST['nickname']
                if len(request.POST['password']) != 0:
                    s.password=password_md5(request.POST['password'])
                if len(request.POST['school']) != 0:
                    s.school=request.POST['school']
                if len(request.POST['email']) != 0:
                    s.email=request.POST['email']
                s.save()
                return HttpResponseRedirect('/')
    if('username' in request.session.keys()):
        context = {'error_message': error_message,'logined': 1, 'name': request.session['username']}
    else:
        return HttpResponse("You should login first.")
    return render(request, 'modify.html',context)

