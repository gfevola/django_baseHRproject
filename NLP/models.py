from django.db import models

# Create your models here.

   
class SurveyData(models.Model):
    Category = models.CharField(max_length = 200,default="N/A")
    ResponseType = models.CharField(max_length = 300,default="N/A")
    EmpID = models.CharField(max_length = 100,default="N/A")
    DeptID = models.CharField(max_length = 1000,default="N/A")
    QuestionID =  models.CharField(max_length = 100,default="N/A")
    QuestionText = models.CharField(max_length = 1000,default="N/A")
    Score = models.IntegerField(default=0)
    TextValue = models.CharField(max_length = 70000,default="N/A")
    TopicID = models.IntegerField(default=0)
    TopicStrength = models.DecimalField(max_digits=10,decimal_places=3,default=0)


class SurveyTopic(models.Model):
    GenID = models.CharField(max_length = 20,default="N/A")
    TopicID = models.IntegerField(default=0)
    Word = models.CharField(max_length = 1000,default="N/A")
    WordPct = models.DecimalField(max_digits=10,decimal_places=3,default=0)