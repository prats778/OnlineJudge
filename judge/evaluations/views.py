from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from django.urls import reverse
from django.views import generic
import os, filecmp

from .models import Problem, Solution
# Create your views here.

def problems(request):
    problems_list = Problem.objects.all()
    context = {'problems_list': problems_list}
    print(context)
    return render(request, 'evaluations/index.html',context)

def problemDetail(request, problem_id):
    problem = get_object_or_404(Problem,pk=problem_id)
    return render(request,'evaluations/detail.html',{'problem':problem}) 

def submitProblem(request,problem_id):
    print(request.FILES)
    f = request.FILES['solution']
    with open('C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\submission.cpp','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    os.system('g++ C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\submission.cpp')
    os.system('a.exe < C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\input.txt > C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\output.txt')

    out1 ='C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\output.txt'
    out2 ='C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\actual_out2.txt'
    if(filecmp.cmp(out1,out2,shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'

    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = 'C:\\Users\\asus\\Desktop\\my_work\\OnlineJudge\\judge\\evaluations\\folders\\solution.cpp'
    solution.save()
    return HttpResponseRedirect(reverse('evaluations:leaderboard'))

def leaderboard(request):
    solutions = Solution.objects.all()
    return render(request, 'evaluations/leaderboard.html',{'solutions':solutions})