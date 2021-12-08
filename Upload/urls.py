from django.urls import path
from . import views

urlpatterns = [
	path('general/',views.generalUpload, name='genUpload'),
	path('full/',views.fullUpload, name='fullUpload'),	
    path('SNA/',views.Upload_SNA, name='snaUpload'),
]