from django.contrib import admin
from .models import Problem,Solution,Testcases
# Register your models here.

admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Testcases)