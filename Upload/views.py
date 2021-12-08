from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect

from .models import Document, BUSL_Mapping, Demographic, Terminations, Hires, Transfers, LOA_Mapping, XFRAction_Mapping, HROps_Headcount, JobCodeTable, SNA_Network, AddressGeo
                            
from .forms import DocumentForm, DocText, DemoForm

import csv, io
import sys
from datetime import datetime, timedelta
import pandas as pd
from django.conf import settings


def ApplyBUMapping(df,doublesided):
    
    BUdata = BUSL_Mapping.objects.all()
    BUdata = pd.DataFrame(BUdata.values()) 
    if doublesided==False:
        df = df.drop(columns=['DepartmentName','Region','ServiceLine','BusinessUnit'])
        df2 = df.merge(BUdata,left_on="DeptID",right_on="DeptID")
    else:
        df = df.drop(columns=['DepartmentName_From','Region_From','ServiceLine_From','BusinessUnit_From',
                                        'DepartmentName_To','Region_To','ServiceLine_To','BusinessUnit_To'])

        df0 = df.merge(BUdata,left_on="DeptID_From",right_on="DeptID")  
        df1 = df0.merge(BUdata,left_on="DeptID_To",right_on="DeptID",suffixes=("","_From"))  
        df2 = df1.merge(BUdata,left_on="DeptID_To",right_on="DeptID",suffixes=("","_To"))  
        
        df2.drop(columns=BUdata.columns.values)

    return(df2)

def generalUpload(request):
    #Gateway to the 'Process Uploads' function
    if request.method == 'POST':
    
        if request.POST['reportname']!="":
            Process_Uploads(request.POST['reportname'])
		
        #job code table
        if request.FILES['jobcodeFile']!="":
            jobcodefile = Document(docfile = request.FILES['jobcodeFile'])
            jobcodefile.save()
            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(jobcodefile.docfile)
            
            history = JobCodeTable.objects.all()
            history.delete()
            
            jobcodeData = pd.read_excel(path)
            for index, row in jobcodeData.iterrows():
                    foo = JobCodeTable(JobCode = row['Job Code'],
                                        JobTitle = row['Job Title'],
                                        StdHrs = row['Std Hrs'],
                                        SalaryPlan = row['Salary Plan'],
                                        Grade = row['Grade'],
                                        UnionCode = row['Union Code'],
                                        FLSA = row['FLSA'],
                                        JobFunction = row['Job Function'],
                                        JobFamily = row['Job Family'],
                                        JobGroup = row['Job Group'],
                                        MgrLvl = row['Manager Level'],
                                        OccupCode = row['Occup Class Code'],
                                        WorkersComp = row['Wrkrs Comp'],
                                        PTOCode = row['PTO/ Vac Code'],
                    )
                    foo.save()
            print('Uploaded Addresses File')

        
        #addresses
        if request.POST['addrType']!="":
            addrFile = Document(docfile = request.FILES['addrFile'])
            addrFile.save()
            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(addrFile.docfile)
            
            history = AddressGeo.objects.all()
            
            addrData = pd.read_excel(path)

            for index, row in addrData.iterrows():
                item = history.filter(LocationName = row['Location Name'])
                if pd.notnull(item):
                    if row['Lat']>0:
                        if isinstance(row['EmpId'],str):
                            y = row['EmpId']
                        else:
                            y = str(row['EmpId'])
                            
                        foo = AddressGeo(LocCategory =  request.POST['addrType'],
                                            LocationName = row['Location Name'],
                                            Address_Street = row['Address'],
                                            Address_City = row['City'],
                                            Address_State = row['State'],
                                            Address_ZipCode = row['Zip Code'],
                                            Latitude = row['Lat'],
                                            Longitude = row['Lon'],
                                            EmpId = y,
                        )
                        foo.save()
            print('Uploaded Addresses File')
            
    else:
        pass
        
    return render(request,
        'Upload/general.html',
    )


def Upload_Demographic(request):
            #save to workbooks model
            newDemofile = Document(docfile = request.FILES['Demofile'])
            newDemofile.save()
			
			#save to Demographic data model
            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newDemofile.docfile)
            repdate = pd.to_datetime(request.POST['reportname'],format="%m/%d/%Y")
               
            #Remove History
            history = Demographic.objects.filter(ReportDate = repdate)
            history.delete()
            name  = str(newDemofile.docfile)
            
            if name[-4:-1].upper() == ".CS":
                with open(path,newline='') as csvfile:
                    demodata = pd.read_csv(csvfile,index_col=False)
                    
            else:
                demodata = pd.read_excel(path) 
                
            if len(demodata.columns.values)<80: #old demographic
                for index, row in demodata.iterrows():
                    foo = Demographic(ReportDate = repdate,
                                        Emplid=row["Emplid"],
                                        Region=[''], #not in regular demographic
                                        BusinessUnit=row["Business Unit"],
                                        DeptID=row["DeptID"],
                                        DepartmentName =row["Department Name"],
                                        ServiceLine =[''], #
                                        WorkLocationCode =row["Work Location Code"],
                                        EmployeeName =row["Employee Name"],
                                        PositionNumber =[''], #
                                        JobCode =row["Job Code"],
                                        UnionCd =row["Union Cd"],
                                        RegTemp =row["Reg/ Temp"],
                                        FTPTPD =row["FT/ PT/ PD"],
                                        StdHrs =row["Std Hrs"],
                                        FTE =row["FTE"],
                                        JobFunctionFamily=row["Job Function/ Family"],
                                        MgrLvl =row["Mgr Lvl"],
                                        HireDate =row["Hire Date"],
                                        ReportsToName =row["Reports To Name"],
                                        ReportsToEmplid =[''], #
                                        ReportsToPositionnumber =[''], #
                                        WorkEmail =row["Work Email"],
                                        Gender =row["Gender"],
                                        EthnicityRace =row["Ethnicity/Race"])
                    foo.save()                   
            else:                            
                for index, row in demodata.iterrows():
                    foo = Demographic(ReportDate = repdate,
                                        Emplid=row["Emplid"],
                                        Region=row["Region"], #not in regular demographic
                                        BusinessUnit=row["Business Unit"],
                                        DeptID=row["DeptID"],
                                        DepartmentName =row["Department Name"],
                                        ServiceLine =row["Service Line"], #
                                        WorkLocationCode =row["Work Location Code"],
                                        EmployeeName =row["Employee Name"],
                                        PositionNumber =row["Position Number"], #
                                        JobCode =row["Job Code"],
                                        UnionCd =row["Union Cd"],
                                        RegTemp =row["Reg/ Temp"],
                                        FTPTPD =row["FT/ PT/ PD"],
                                        StdHrs =row["Std Hrs"],
                                        FTE =row["FTE"],
                                        JobFunctionFamily=row["Job Function/ Family"],
                                        MgrLvl =row["Mgr Lvl"],
                                        HireDate =row["Hire Date"],
                                        ReportsToName =row["Reports To Name"],
                                        ReportsToEmplid =row["Reports To Emplid"], #
                                        ReportsToPositionnumber =row["Reports To Position number"], #
                                        WorkEmail =row["Work Email"],
                                        Gender =row["Gender"],
                                        EthnicityRace =row["Ethnicity/Race"])
                                        

                    foo.save()


def Upload_Terminations(request):
			#save to Terms data model     
            newTermfile = Document(docfile = request.FILES['Termfile'])
            newTermfile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newTermfile.docfile)
            #remove all history before saving
            history = Terminations.objects.all()
            history.delete() 
 
            with open(path,newline='') as csvfile:
                termdata = pd.read_csv(csvfile)
 
                for index, row in termdata.iterrows():
                    foo = Terminations(Emplid=row["Emplid"],
                                        TermDate =pd.to_datetime(row["Term Date"],format="%m/%d/%Y"),
                                        Region=row["Region"],
                                        BusinessUnit=row["Business Unit"],
                                        DeptID=row["DeptID"],
                                        DepartmentName =row["Department Name"],
                                        ServiceLine =row["Service Line"],
                                        WorkLocationCode =row["Work Location Code"],
                                        EmployeeName =row["Employee Name"],
                                        PositionNumber =row["Position Number"],
                                        JobCode =row["Job Code"],
                                        UnionCd =row["Union Cd"],
                                        RegTemp =row["Reg/ Temp"],
                                        FTPTPD =row["FT/ PT/ PD"],
                                        StdHrs =row["Std Hrs"],
                                        FTE =row["FTE"],
                                        JobFunctionFamily=row["Job Function/ Family"],
                                        MgrLvl =row["Mgr Lvl"],
                                        HireDate =row["Hire Date"],
                                        ReportsToName =row["Reports To Name"],
                                        ReportsToEmplid =row["Reports To Emplid"],
                                        ReportsToPositionnumber =row["Reports To Position number"],
                                        WorkEmail =row["Work Email"],
                                        Gender =row["Gender"],
                                        EthnicityRace =row["Ethnicity/Race"],
                                        TermReasonCategory = row["Term Vol or Invol"],
                                        ActionReason = row["Term Reason Code"],
                                        ActionReasonDesc = row["Term Reason Description"])

                    foo.save()


def Upload_Hires(request):
			#save to Hires data model     
            newHirefile = Document(docfile = request.FILES['Hirefile'])
            newHirefile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newHirefile.docfile)
            #remove all history before saving
            history = Hires.objects.all()
            history.delete() 
 
            with open(path,newline='') as csvfile:
                hiredata = pd.read_csv(csvfile)
 
                for index, row in hiredata.iterrows():
                    if row["Rehire Date"][:2]!="  ":
                        foo = Hires(Emplid = row["Empl ID"],
                                        RehireDate = pd.to_datetime(row["Rehire Date"],format="%m/%d/%Y"),
                                        Region = row["Region"],
                                        BusinessUnit = row["Business Unit"],
                                        DeptID = row["DeptID"],
                                        DepartmentName = row["Department Name"],
                                        ServiceLine = row["Service Line"],
                                        WorkLocationCode = [''],
                                        EmployeeName = row["Employee Name"],
                                        PositionNumber = row["Position Nbr"],
                                        JobCode = row["Job Code"],
                                        UnionCd = row["Union Code"],
                                        RegTemp = row["Reg /Temp"],
                                        FTPTPD = row["FT / PT / PD"],
                                        StdHrs = row["Std Hours"],
                                        FTE = row["FTE"],
                                        JobFunctionFamily = row["Job Family"],
                                        MgrLvl = row["Manager Level"],
                                        HireDate = row["Hire Date"],
                                        ReportsToName = row["Reports To Name"],
                                        ReportsToEmplid = [''],
                                        ReportsToPositionnumber =[''],
                                        WorkEmail = [''],
                                        Gender =[''],
                                        EthnicityRace =[''],
                                        ActionReason = row["Action / Reason"],
                                        ActionReasonDesc = row["Action Reason Description"])
                        foo.save()


def Upload_Transfers(request):
			#save to Hires data model     
            newXFRfile = Document(docfile = request.FILES['XFRfile'])
            newXFRfile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newXFRfile.docfile)
            #remove all history before saving
            history = Transfers.objects.all()
            history.delete() 
 
            with open(path,newline='') as csvfile:
                XFRdata = pd.read_csv(csvfile)
 
                for index, row in XFRdata.iterrows():
                    #if row["Rehire Date"][:2]!="  ":
                        foo = Transfers(Emplid = row['Empl ID'],
                                            ActionReason = row['Action / Reason'],
                                            ActionReasonDesc = row['Action Reason Descr'],
                                            EmployeeName = row['Employee Name'],
                                            EffectiveDate = pd.to_datetime(row["Effective Date"],format="%m/%d/%Y"),
                                            Region_From = [''],
                                            BusinessUnit_From = row['PRIOR Business Unit'],
                                            DeptID_From = row['PRIOR DeptID'],
                                            DepartmentName_From = row['PRIOR Department Name'],
                                            ServiceLine_From = [''],
                                            WorkLocationCode_From = [''],
                                            PositionNumber_From = row['PRIOR Position Nbr'],
                                            JobCode_From = row['PRIOR Job Code'],
                                            UnionCd_From = row['PRIOR Union Code'],
                                            RegTemp_From = row['PRIOR Reg /Temp'],
                                            FTPTPD_From = row['PRIOR FT / PT / PD'],
                                            StdHrs_From = row['PRIOR Std Hours'],
                                            FTE_From = row['PRIOR FTE'],
                                            JobFunctionFamily_From = [''],
                                            MgrLvl_From = [''],
                                            Region_To = [''],
                                            BusinessUnit_To = row['CURRENT Business Unit'],
                                            DeptID_To = row['CURRENT DeptID'],
                                            DepartmentName_To = row['CURRENT Department Name'],
                                            ServiceLine_To = [''],
                                            WorkLocationCode_To = [''],
                                            PositionNumber_To = row['CURRENT Position Nbr'],
                                            JobCode_To = row['CURRENT Job Code'],
                                            UnionCd_To = row['CURRENT Union Code'],
                                            RegTemp_To = row['CURRENT Reg /Temp'],
                                            FTPTPD_To = row['CURRENT FT / PT / PD'],
                                            StdHrs_To = row['CURRENT Std Hours'],
                                            FTE_To = row['CURRENT FTE'],
                                            JobFunctionFamily_To = [''],
                                            MgrLvl_To = [''])

                        foo.save()


def Upload_BUSLMappingFile(request):
			#save to BU data model     
            newBUfile = Document(docfile = request.FILES['BUSLfile'])
            newBUfile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newBUfile.docfile)
            #remove all history before saving
            history = BUSL_Mapping.objects.all()
            history.delete() 

            with open(path,newline='') as xlsfile:
                BUdata = pd.read_csv(xlsfile)
 
                for index, row in BUdata.iterrows():
                    foo = BUSL_Mapping(UploadDate = datetime.now(),
                                        DeptID=row["Dept ID"],
                                        DepartmentName=row["Dept Description"],
                                        BusinessUnit=row["Bus Unit"],
                                        BUDescription=row["BU Description"],
                                        Region_HROps=row["Region (for HR Ops Dashboard)"],
                                        Region=row["Region (for Regular Report)"],
                                        BU_SL=row["Service Line (for Regular Report)"])
                                        
                    foo.save()
  
  
def Upload_LOA_XFRFiles(request):
			#save to BU data model     
            newLOAfile = Document(docfile = request.FILES['LOAfile'])
            newLOAfile.save()

            path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newLOAfile.docfile)
            #remove all history before saving
            history = LOA_Mapping.objects.all()
            history.delete() 
            
            history = XFRAction_Mapping.objects.all()
            history.delete() 

            #with open(path,newline='') as xlsfile:
            LOAdata = pd.read_excel(path,"LOA Bucket Lookup")
            XFRActdata = pd.read_excel(path,"TXF Action Reason lookup")
                
            ReasonCodes = LOAdata.iloc[2:,4:7].drop_duplicates()
            ReasonCodes.columns = ["Reason Code","Reason Desc","Bucket"]
           
            XFRCodes = XFRActdata.iloc[1:,1:3].drop_duplicates()
            XFRCodes.columns = ["XFR Reason","XFR Type"]
            
            #LOA
            for index, row in ReasonCodes.iterrows():
                    foo = LOA_Mapping(ReasonCode=row["Reason Code"],
                                        ReasonDesc=row["Reason Desc"],
                                        ReasonBucket=row["Bucket"])

                    foo.save()
                    
            #XFR Action
            for index, row in XFRCodes.iterrows():
                    foo = XFRAction_Mapping(TransferReason=row["XFR Reason"],
                                      TransferType=row["XFR Type"])
                    foo.save()


def Upload_SNA(request):

    if request.method == 'POST':
        print(request.FILES)
        newSNAfile = Document(docfile = request.FILES['SNAfile'])
        newSNAfile.save()
        path = settings.MEDIA_ROOT.replace("\\","/") + "/"+ str(newSNAfile.docfile)
        
        history = SNA_Network.objects.filter(ModelIndex=request.POST['ModelName'])
        history.delete() 
        
        with open(path,newline='') as xlsfile:
            SNAdata = pd.read_csv(xlsfile)		
            for index, row in SNAdata.iterrows():
                foo = SNA_Network(ModelIndex =  request.POST['ModelName'],
                       Sender = row['Sender'],
                       Recipient = row['Recipient'],
                       N = row['Count'],
                       Department = row['DeptName'],
                       #JobFunction = row['JobFunction'],
                       Betweenness = row['Betweenness'],
                       Closeness = row['Closeness'],
                )
                foo.save()
    else:
        pass
        
    return render(request,
        'Upload/uploadSNA.html',
    )
        

#################full upload################
def fullUpload(request):
    #form = DemoForm(request.POST,request.FILES)


    #0. Import BU/SL
    if 'BUSL_submit' in request.POST:
        Upload_BUSLMappingFile(request)

    #1. Import Demographic       
    if ('SubmitAll' in request.POST) or ('Demo_submit' in request.POST): 
        Upload_Demographic(request) 
                    
    #2. Import Terminations
    if ('SubmitAll' in request.POST) or ('Term_submit' in request.POST): 
        Upload_Terminations(request)  

    #3. Import Hires
    if ('SubmitAll' in request.POST) or ('Hire_submit' in request.POST): 
        Upload_Hires(request)  

    #4. Import Transfers
    if 'XFR_submit' in request.POST:
        Upload_Transfers(request)

    #5. Import LOA/XFR Mapping
    if 'LOA_submit' in request.POST:
        Upload_LOA_XFRFiles(request)

    print("Completed Upload")
    
    return render(request,
        'Upload/full.html'
	)


def Process_Uploads(rdate):
    #Gather Data from Models
    
    #effective date 
    rdate = pd.to_datetime(rdate,format="%m/%d/%Y")
    pdate = rdate - timedelta(days=365)

    #---re-import dataset---
    #*Demographic
    demo = Demographic.objects.all()
    demo1 = Demographic.objects.filter(ReportDate="2018-08-31")
    
    demoDF = pd.DataFrame(demo.values())
    demoDF = ApplyBUMapping(pd.DataFrame(demo.values()),False)
    
    demoDF['TermDate']=pd.to_datetime(demoDF['ReportDate'],format="%Y-%m-%d") #copy to same-named column for merge, convert from object to date
        
    #*Terms
    term = Terminations.objects.filter(TermDate__gte = (rdate - timedelta(days=365))).filter(TermDate__lte = rdate)
    termDF = ApplyBUMapping(pd.DataFrame(term.values()),False) 
     
    #*Hires
    hire = Hires.objects.filter(RehireDate__gte = (rdate - timedelta(days=365))).filter(RehireDate__lte = rdate)
    hireDF = ApplyBUMapping(pd.DataFrame(hire.values()),False) 
    
    #*Transfers
    transfer = Transfers.objects.filter(EffectiveDate__gte = (rdate - timedelta(days=365))).filter(EffectiveDate__lte = rdate)
    xfrDF = ApplyBUMapping(pd.DataFrame(transfer.values()),True) 
    
    #Add Transfer Type Mapping
    xfrmap = XFRAction_Mapping.objects.all()
    xfrmap = pd.DataFrame(xfrmap.values())
    
    xfrDF = xfrDF.merge(xfrmap,left_on = "ActionReasonDesc",right_on="TransferReason",how="left")
    xfrDF = xfrDF[xfrDF.TransferType.notnull()]

    values1 = ['Category','Region','BU_SL']
    values2 = ['Category','Region']
    values3 = ['Category']
    
    cat1 = "BU/SL"
    cat2 = "Region"
    cat3 = "System-Wide"
    
    def TurnoverCalc(values,category):
        #Summarizes by columns in "values", should line up with category description
        #Carry over existing dataframe variables
        
        demoDF['Category'] = category
        termDF['Category'] = category
        hireDF['Category'] = category
        xfrDF['Category_From'] = category
        
        xfrvalues = []
        for i in values:
            xfrvalues.append(i+"_From")

        ###########
        #Demographic Turnover filter criteria

        crit1 = (demoDF.RegTemp == "R")    
        crit2 = (demoDF.JobFunctionFamily != "PHY_AE")  
        crit3 = (demoDF.FTPTPD != "C")    
        crit4 = (demoDF.UnionCd != "203")  

        crit5 = (termDF.RegTemp == "R")    
        crit6 = (termDF.JobFunctionFamily != "PHY_AE")  
        crit7 = (termDF.FTPTPD != "C")    
        crit8 = (termDF.UnionCd != "203") 
        crit9 = (termDF.BusinessUnit != "FLEXN") 
        crit10 = (~termDF.ActionReason.isin(["WRK","CNV"])) 
        
        crit11 = (hireDF.RegTemp == "R") 
        crit12 = (hireDF.JobFunctionFamily != "PHY_AE")  
        crit13 = (hireDF.FTPTPD != "C")
        crit14 = (~hireDF.ActionReason.isin(["CN1","HAQ","HS1","OPT"]))
        
        
        #pivot PAD data
        term_headcount = termDF[values + ['Emplid']][crit5 & crit6 & crit7 & crit8 & crit9 & crit10][termDF.TermReasonCategory=="Voluntary"].groupby(values).count().reset_index()  #pd.Grouper(key='TermDate',freq="M")
        hires_headcount = hireDF[values + ['Emplid']][crit11 & crit12 & crit13 & crit14].groupby(values).count().reset_index()
        xfr_headcount = xfrDF[xfrvalues + ['Emplid']].groupby(xfrvalues).count().reset_index()
        
        #pivot xfr by transfer type (promotion, lateral, etc.)
        xfr_hcByType = xfrDF[xfrvalues + ['Emplid'] + ['TransferType']].groupby(xfrvalues + ['TransferType']).count().reset_index()
        xfr_hcByType = xfr_hcByType.groupby(xfrvalues + ['TransferType'])['Emplid'].sum().unstack('TransferType')
        xfr_hcByType = xfr_hcByType.reset_index()

        #Pivot Demographic
        df_headcount = pd.DataFrame(demoDF[values + ['TermDate','Emplid']].groupby(values + ['TermDate']).count().reset_index())
        
        df_hcTermCalc = pd.DataFrame(demoDF[values + ['TermDate','Emplid']][crit1 & crit2 & crit3 & crit4].groupby(values + ['TermDate']).count().reset_index())  
        df_hcTermCalc = df_hcTermCalc[df_hcTermCalc.TermDate==rdate].merge(df_hcTermCalc[df_hcTermCalc.TermDate==pdate],left_on=values,right_on=values,how="inner",suffixes=('CY','PY'))     
        
        ###############
        #Subset full to CY only and w/ filtered
        df_headcount = df_headcount[df_headcount.TermDate==rdate].merge(df_hcTermCalc,left_on=values,right_on=values,how="outer",suffixes=('Full',''))
        print(df_headcount.head())
        df_headcount['Emplid'] = (df_headcount.EmplidCY + df_headcount.EmplidPY)/2
        df_headcount = df_headcount.drop(columns=['TermDateCY','TermDatePY'])

        
        #Merge Files
        DemoTurnover = df_headcount.merge(hires_headcount,left_on=values,right_on=values,how="left",suffixes=('','Hire'))
        DemoTurnover = DemoTurnover.merge(xfr_hcByType,left_on=values,right_on=xfrvalues,how="left",suffixes=('','XFR'))
        
        DemoTurnover = DemoTurnover.merge(term_headcount,left_on=values,right_on=values,how="left",suffixes=('Demo','Term'))
        DemoTurnover['TurnoverPct'] = DemoTurnover['EmplidTerm']/DemoTurnover['EmplidDemo']
        DemoTurnover['ReportDate'] = rdate
        
        DemoTurnover = DemoTurnover.drop(columns=xfrvalues + ['TermDate'])
        

        #add if columns don't exist
        if not 'Lateral' in DemoTurnover.columns:
            DemoTurnover['Lateral'] = 0
            
        if not 'Promotion' in DemoTurnover.columns:
            DemoTurnover['Promotion'] = 0
            
        if not 'Demotion' in DemoTurnover.columns:
            DemoTurnover['Demotion'] = 0
        
        DemoTurnover[['EmplidDemo','EmplidCY','EmplidPY','EmplidHire','EmplidTerm','Lateral','Demotion','Promotion','TurnoverPct']] = DemoTurnover[['EmplidDemo','EmplidCY','EmplidPY','EmplidHire','EmplidTerm','Lateral','Demotion','Promotion','TurnoverPct']].fillna(0)
        
        
        return(DemoTurnover)
        ####end subfunction#########################
        
    #run function
    y3 = TurnoverCalc(values3,cat3)
    y2 = TurnoverCalc(values2,cat2)
    y1 = TurnoverCalc(values1,cat1)
    y = pd.concat([y3,y2,y1],sort=True)
         
         #Save output
   # writer = pd.ExcelWriter('C:\\Users\\gfevola\\Documents\\Testing\\Proj2 Output.xlsx')
   # demoDF[values + ['TermDate','Emplid']][crit1 & crit2 & crit3 & crit4].to_excel(writer,'Demographic',index=False)
   # termDF[crit5 & crit6 & crit7 & crit8 & crit9 & crit10].to_excel(writer,'Terms',index=False)
   # y.to_excel(writer,"HROps",index=False)
   # writer.save() 
    
    #save to model
    history = HROps_Headcount.objects.filter(ReportDate = rdate)
    history.delete() #delete old data for report date
        
    for index, row in y.iterrows():
            foo = HROps_Headcount(ReportDate = rdate,
                                    Category = row['Category'],
                                    Region = row['Region'],
                                    BU_SL = row['BU_SL'],
                                    Headcount_Demographic_Full = row['EmplidDemo'],
                                    Headcount_Demographic_CYFiltered = row['EmplidCY'],
                                    Headcount_Demographic_PYFiltered = row['EmplidPY'],
                                    Headcount_Hires_TTM = row['EmplidHire'],
                                    Headcount_Terms_TTM = row['EmplidTerm'],
                                    Headcount_XFRs_TTM = row['Lateral']+ row['Promotion'] + row['Demotion'],
                                    Headcount_XFR_Lateral_TTM = row['Lateral'],
                                    Headcount_XFR_Promotion_TTM = row['Promotion'],
                                    Headcount_XFR_Demotion_TTM = row['Demotion'],
                                    TurnoverPct_TTM = row['TurnoverPct'])
            foo.save()
            
    print("Completed Stats")

