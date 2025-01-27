import time
from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    submit = models.IntegerField()
    ac = models.IntegerField()
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Testcase(models.Model):
    def upload_path(instance, filename):
        return "testcases/{}/{}".format(instance.problem.id, filename)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.FileField(upload_to=upload_path)
    output = models.FileField(upload_to=upload_path)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()

    def __str__(self):
        return self.problem.title

class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=30)
    school = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    submit = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    root = models.BooleanField(default=False)

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

    stat = models.TextField(default=stat_default())
    ips = models.TextField(default=[])

    def __str__(self):
        return self.username

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.TextField()
    language = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    time_used = models.IntegerField()
    memory_used = models.IntegerField()
    length = models.IntegerField()
    submit_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    from_contest = models.IntegerField(default=0)
    from_contest_problem = models.CharField(max_length=10,default='0')
    contest_start_time = models.DateTimeField(default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8)))
    contest_end_time = models.DateTimeField(default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+3600*8)))

    def __str__(self):
        return self.source

class Waiting(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.submission.source
