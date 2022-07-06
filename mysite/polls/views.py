from asyncio import selector_events
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from matplotlib.pyplot import get
from .models import Question,Choice
from django.urls import reverse

# Create your views here.

def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context ={
        'latest_question_list':latest_question_list
    }
    output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output);
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    # try:
    #     question=Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404("question does not exist")
    question=get_object_or_404(Question,pk=question_id);

    return render(request, 'polls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id);

    return render(request,'polls/results.html',{'question':question})
    return HttpResponse("ur looking at results of question id %s " % question_id);

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):   
        return render(request,'polls/detail.html',{'question':question,'error_message':'You did not select a choice'})
    else:
        selected_choice.votes+=1;
        selected_choice.save();    
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
    return HttpResponse("ur voting on question id %s " % question_id);
