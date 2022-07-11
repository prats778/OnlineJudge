from django.db import models

# Create your models here.

class Problem(models.Model):
    name=models.CharField(max_length=200)
    problem_statement=models.CharField(max_length=255)
    code=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Solution(models.Model):
    problem= models.ForeignKey(Problem, on_delete=models.CASCADE)
    # submitted_by=models.charField(mask_length=50)
    verdict= models.CharField(max_length=50)
    submitted_at = models.CharField(max_length=50)
    submitted_code = models.CharField(max_length=255)

    def __str__(self):
        return self.verdict

class Testcases(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return self.input        
    