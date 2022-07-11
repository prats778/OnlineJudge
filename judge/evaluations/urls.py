from django.urls import path
from . import views

app_name= 'evaluations'

urlpatterns = [
    path('',views.problems,name='problems'),
    path('problem/<int:problem_id>/',views.problemDetail,name='problem_detail'),
    path('problem/<int:problem_id>/submit/',views.submitProblem,name='submit'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('evaluations/',views.problems,name='evaluations'),
] 