from django.urls import path
from . import views

urlpatterns = [
	path('importText/',views.Upload_Survey, name='importSurvey'),
    path('survey/',views.View_SurveyResults, name='Surveyoutput')
]