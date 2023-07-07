from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from django.urls import reverse
from django.views import generic
import os, filecmp 
from django import forms
from .models import Problem, Solution
import shlex
import subprocess
from subprocess import PIPE, run
from subprocess import check_call,check_output, STDOUT
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
    # print(request.POST['code'])
    f=0
    flag=0
    if len(request.POST['code']):
        print("kuch hai")
        f=request.POST['code']
        flag=1
    else:
        print("khali hai")
        f=request.FILES['solution']      
        
    # f = request.FILES['solution']
    # os.system('cd evaluations/folders')

    # print("current directory working ==> ", os.getcwd())

    docker_path=os.path.join(os.getcwd(), 'evaluations/folders')

    print("docker directory working ==> ", os.getcwd())
    with open(os.path.join(docker_path,'submission.cpp'),'wb+') as dest:
        if not flag:
            for chunk in f.chunks():
                dest.write(chunk)
        else:
            print("executing code")
            code=request.POST['code']
            code=code.encode()
            dest.write(code);
    
    os.system('echo $MY_SUDO_PASS | sudo -S docker build . -t docker-compiler -f evaluations/folders/dockerfile')
    print("Code Testing Started")
    input_file=os.path.join(docker_path,'input.txt')
    output_file=os.path.join(docker_path,'output.txt')
    error_file=os.path.join(docker_path,'error.txt')

    print("Input file ==>",input_file)
    print("Output file ==>",output_file)
    print("Error file ==>",error_file)

    with open(input_file,'r') as file, open(output_file, 'w') as outfile , open(error_file,'w') as errfile:
        # os.system('echo $MY_SUDO_PASS | sudo -S docker run -i docker-compiler /bin/bash -c "g++ evaluations/folders/submission.cpp; ./a.out < evaluations/folders/input.txt > evaluations/folders/output.txt;cat evaluations/folders/output.txt"')
        # subprocess.check_call(shlex.split("sudo docker run -i docker-compiler python evaluations/folders/test_docker.py"), stdin=file, stdout=outfile, stderr=errfile,timeout=15)
      subprocess.check_call(shlex.split("sudo docker run -id --name main_container docker-compiler"))
      subprocess.check_call(shlex.split("sudo docker exec -i main_container python evaluations/folders/test_docker.py"), stdin=file, stdout=outfile, stderr=errfile,timeout=15)
    #   subprocess.check_call(shlex.split("sudo docker exec main_container g++ evaluations/folders/submission.cpp"),stderr=errfile)
    #   subprocess.check_call(shlex.split("sudo docker exec -i main_container ./a.out "),stdin=file, stdout=outfile, stderr=errfile, timeout=15) 
    print("Compiled Successfully Generated Output")       
    # Open a file: file
    file = open('evaluations/folders/output.txt',mode='r')

    # read all lines at once
    all_of_it = file.read()

    # close the file
    file.close()

    print("Output ==> ", all_of_it)



    out1 = os.path.join(docker_path,'actual_out2.txt')
    if(filecmp.cmp(out1,output_file,shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'



    subprocess.check_call(shlex.split("sudo docker stop main_container"))
    subprocess.check_call(shlex.split("sudo docker rm main_container"))

    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = 'solution.cpp'
    solution.save()
    return HttpResponseRedirect(reverse('evaluations:leaderboard'))

def leaderboard(request):
    solutions = Solution.objects.all()
    return render(request, 'evaluations/leaderboard.html',{'solutions':solutions})