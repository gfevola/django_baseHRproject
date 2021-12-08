from django.shortcuts import render
from .forms import SurveyTextForm
from .models import SurveyData, SurveyTopic
from Upload.forms import Document
from Upload.models import Demographic, BUSL_Mapping
from django.conf import settings

from .scripts import createLDA

import pandas as pd
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.utils.safestring import mark_safe

# Create your views here.
def Upload_Survey(request):
    
    if request.method == 'POST':
            NLPFile = Document(docfile = request.FILES['NLPfile'])
            NLPFile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(NLPFile.docfile)
            
            #delete old versions (for now)
            history = SurveyData.objects.all()
            history.delete() 
            
            history = SurveyTopic.objects.all()
            history.delete()             
            
 
            #with open(path,newline='') as xlfile:
            Surveydatafile = pd.read_excel(path)
 
            #main function
            ldaoutput = createLDA(Surveydatafile)
            
            for index, row in ldaoutput[0].iterrows():
                    foo = SurveyData(Category = row['Category'],
                                        ResponseType = row['Response Type'],
                                        EmpID = row['ID'],
                                        DeptID = row['DeptID'],
                                        QuestionID = row['Question.No'],
                                        QuestionText = row['variable'],
                                        Score = row['Score'], 
                                        TextValue = row['value'],
                                        TopicID = row['Topic'],
                                        TopicStrength = row['TopicStrength']
                                        )
                    foo.save()
            
            for index, row in ldaoutput[1].iterrows():
                    foo = SurveyTopic(GenID = request.POST["IDtext"],
                                        TopicID = row['TopicNo'],
                                        Word = row['Word'],
                                        WordPct = row['WordPct']
                                        )
                    foo.save()          
            
            print(ldaoutput)
            
    else:
        pass
        
    return render(request,"NLP/uploadSimple.html")
    
    
def View_SurveyResults(request):
    #using hardcoded demographic date
    
    data_survey = SurveyData.objects.all().only("Category","QuestionID","QuestionText","TopicID","TopicStrength")
    data_BU = BUSL_Mapping.objects.all()
    data_topics = SurveyTopic.objects.all() #filter(GenID="wefuh83")
    
    data_survey = pd.DataFrame(data_survey.values())
    data_BU = pd.DataFrame(data_BU.values())
    data_topics = pd.DataFrame(data_topics.values())
    
    datamerge = data_survey.merge(data_BU,left_on="DeptID",right_on="DeptID")
    data = datamerge.replace('"',"",regex=True).to_json(orient="records").replace("'","").replace("\\", "-").replace("/","-")
    topics = data_topics.to_json(orient="records").replace("'","").replace("\\", "-")

    #data  = serializers.serialize("json",data_survey).replace("'","").replace("\\", "-").replace("/", "-").replace('"','')

    #data = json.dumps(data,cls=DjangoJSONEncoder)

    return render(request,'NLP/output.html',{'data' : data, 'topics': topics})
    