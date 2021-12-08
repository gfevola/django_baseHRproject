from django.urls import path
from . import views 


urlpatterns = [
	path('Demographic/',views.visualize_model,name='Visual-test'),
	path('sunburst/',views.visualize_Sunburst,name='Visual-sunburst'),
    path('SNA/',views.visualize_Network,name='Visual-network'),
    path('NorthwellMap/',views.visualize_Map,name='Visual-map'),
]
	
