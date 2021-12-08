from django import forms
from .models import SurveyData

# Create your forms here.

class SurveyTextForm(forms.Form):
	
	class Meta:
		model = SurveyData
		fields = ('Category', 'ResponseType','EmpId', 'QuestionID','QuestionText','TextValue')
