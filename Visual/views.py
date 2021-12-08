from django.shortcuts import render
from Upload.models import Document, Demographic, HROps_Headcount, BUSL_Mapping, SNA_Network, AddressGeo
from Upload.views import ApplyBUMapping
from django.http import HttpResponse

from django.core import serializers

import pandas as pd
from datetime import datetime, timedelta

import csv
import json
from django.conf import settings

	
#return data from model
def visualize_model(request):
    rdate = datetime.today() - timedelta(days=400)
    print(rdate)
  
    data = HROps_Headcount.objects.filter(ReportDate__gte = (rdate - timedelta(days=365))).order_by('ReportDate')
    datajson = serializers.serialize("json",data).replace("'","")

    return render(request,
		'Visual/Modeltest.html',
		{'datarow': datajson}
	)
   

def visualize_Sunburst(request):
    #in testing
    #data = BUSL_Mapping.objects.all()
    TitleFilePath = "C:\\Users\\gfevola\\Documents\\JobCodes_TestforProj2.xlsx"
    data = pd.read_excel(TitleFilePath)
    data = CreateNesting(pd.DataFrame(data[0:70]),["Job Code","Job Title","Job Family","Job Function"])
    data = data[1:]

    datajson = data.to_json(orient="records").replace("'","").replace("\\", "-")
    return render(request, 'Visual/Sunburst3.html', {'data' : datajson})
    

def visualize_Network(request):

    if request.method == 'POST':
        print(request['filter2'])
    
    data = SNA_Network.objects.filter(ModelIndex="HRTest").order_by('Sender')
    
    #Create Alluvial Data
    sender = pd.DataFrame(data.values()).loc[:,'Sender'].unique()
    recipient = pd.DataFrame(data.values()).loc[:,'Recipient'].unique()
    
    #connections b/w departments must be greater than...
    limit= '20'
    
    nodes = pd.DataFrame(pd.concat([pd.DataFrame(sender),pd.DataFrame(recipient)],axis=0).drop_duplicates())
    links = pd.DataFrame(pd.DataFrame(data.values()).query('N>'+limit).loc[:,['Sender','Recipient']])


    for x in range(3):
        nodes = nodes.merge(links,how="left",right_on="Sender",left_on=len(nodes.columns)-1)
        nodes.columns = range(len(nodes.columns))
        #nodes = nodes.drop(columns=len(nodes.columns)-2)
       
    #with pd.ExcelWriter("C:\\Users\\gfevola\\Documents\\Testing\\From Python\\nodestest.xlsx") as writer:
    #        nodes.to_excel(writer)
    
    print(nodes)

    
    data  = serializers.serialize("json",data).replace("'","")
    #data = pd.DataFrame(data)
    #Nodes = data['Sender'].unique()    
    return render(request,'Visual/SNA1.html',{'data' : data})
    
    
def visualize_Map(request):
  
    #demographic - hardcoded report date
    data = Demographic.objects.filter(ReportDate="2019-10-31")
    dataDF = pd.DataFrame(data.values())
    dataDF = ApplyBUMapping(dataDF,False)

    #address
    homeData =  AddressGeo.objects.filter(LocCategory="Home")
    homeDF = pd.DataFrame(homeData.values())[1:3000]

    data = dataDF.merge(homeDF,how="left",left_on="Emplid",right_on="EmpId")
    datajson = data.to_json(orient="records").replace("'","")
      
    workData =  AddressGeo.objects.filter(LocCategory="Work")
    workDF = pd.DataFrame(workData.values())      
    workjson = workDF.to_json(orient="records").replace("'","")

      
    #temporary location data
    geocode_path = "C:\\Users\\gfevola\\Documents\\Testing\\Locations\\Work Locations Geocoded.xlsx"
    geocode_file = pd.read_excel(geocode_path)
    geojson = geocode_file.to_json(orient="records").replace("'","")
    
    return render(request,'Visual/Map.html', {'locs' : workjson , 'data': datajson})
    
    
    
#######helper function#############    
def CreateNesting(df,levels):
    levelsplus = levels + ['Overall']
    pack = pd.DataFrame()

    df['Overall']="Overall"

    for i,x in enumerate(levels):
        col1 = df.loc[:,[x,levelsplus[i+1]]]
        col1.columns = ['child','parent']
        pack = pd.concat([col1,pack],sort=True)

    pack = pack.groupby(pack.columns.tolist()).size().reset_index().rename(columns={0:'Count'})
    #pack = pd.concat(pack,pd.DataFrame(["Overall","",0]),axis=0)
    pack = pack.append(pd.DataFrame([["Overall","",0]],columns=['child','parent','Count']))
    return(pack)
     