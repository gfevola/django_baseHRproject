from django.db import models
from datetime import datetime
from django import forms


# Create your models here.
class Document(models.Model):
	docfile = models.FileField(upload_to='documents')
	

class DataX(models.Model):
	name = models.CharField(max_length=50)
	salary = models.DecimalField(max_digits=10,decimal_places=2,null=True)
	location = models.CharField(max_length=50,null=True)
   
   
class BUSL_Mapping(models.Model):
    UploadDate = models.DateField(("Date"))
    DeptID = models.CharField(max_length = 100)
    DepartmentName = models.CharField(max_length = 300)
    BusinessUnit = models.CharField(max_length = 100)
    BUDescription = models.CharField(max_length = 100)
    Region_HROps = models.CharField(max_length = 100)
    Region = models.CharField(max_length = 100)
    BU_SL = models.CharField(max_length = 100)
    
   
class LOA_Mapping(models.Model):
    ReasonCode = models.CharField(max_length = 10)
    ReasonDesc = models.CharField(max_length = 100)
    ReasonBucket = models.CharField(max_length = 100)
    

class XFRAction_Mapping(models.Model):
    TransferReason = models.CharField(max_length = 100)
    TransferType = models.CharField(max_length = 100)

    
#Peoplesoft Files   
class Demographic(models.Model):
    ReportDate = models.DateField(("Date"))
    Emplid = models.CharField(max_length = 100)
    Region = models.CharField(max_length = 100)
    BusinessUnit = models.CharField(max_length = 100)
    DeptID = models.CharField(max_length = 100)
    DepartmentName = models.CharField(max_length = 100)
    ServiceLine = models.CharField(max_length = 100)
    WorkLocationCode = models.CharField(max_length = 100)
    EmployeeName = models.CharField(max_length = 100)
    PositionNumber = models.CharField(max_length = 100)
    JobCode = models.CharField(max_length = 100)
    UnionCd = models.CharField(max_length = 100)
    RegTemp = models.CharField(max_length = 100)
    FTPTPD = models.CharField(max_length = 100)
    StdHrs = models.CharField(max_length = 100)
    FTE = models.CharField(max_length = 100)
    JobFunctionFamily = models.CharField(max_length = 100)
    MgrLvl = models.CharField(max_length = 100)
    HireDate = models.CharField(max_length = 100)
    ReportsToName = models.CharField(max_length = 100)
    ReportsToEmplid = models.CharField(max_length = 100)
    ReportsToPositionnumber = models.CharField(max_length = 100)
    WorkEmail = models.CharField(max_length = 100)
    Gender = models.CharField(max_length = 100)
    EthnicityRace = models.CharField(max_length = 100)


class Terminations(models.Model):
    Emplid = models.CharField(max_length = 100)
    TermDate = models.DateField(("Date"))
    Region = models.CharField(max_length = 100)
    BusinessUnit = models.CharField(max_length = 100)
    DeptID = models.CharField(max_length = 100)
    DepartmentName = models.CharField(max_length = 100)
    ServiceLine = models.CharField(max_length = 100)
    WorkLocationCode = models.CharField(max_length = 100)
    EmployeeName = models.CharField(max_length = 100)
    PositionNumber = models.CharField(max_length = 100)
    JobCode = models.CharField(max_length = 100)
    UnionCd = models.CharField(max_length = 100)
    RegTemp = models.CharField(max_length = 100)
    FTPTPD = models.CharField(max_length = 100)
    StdHrs = models.CharField(max_length = 100)
    FTE = models.CharField(max_length = 100)
    JobFunctionFamily = models.CharField(max_length = 100)
    MgrLvl = models.CharField(max_length = 100)
    HireDate = models.CharField(max_length = 100)
    ReportsToName = models.CharField(max_length = 100)
    ReportsToEmplid = models.CharField(max_length = 100)
    ReportsToPositionnumber = models.CharField(max_length = 100)
    WorkEmail = models.CharField(max_length = 100)
    Gender = models.CharField(max_length = 100)
    EthnicityRace = models.CharField(max_length = 100)
    TermReasonCategory = models.CharField(max_length = 100)
    ActionReason = models.CharField(max_length = 100)
    ActionReasonDesc = models.CharField(max_length = 100)


class Hires(models.Model):
    Emplid = models.CharField(max_length = 100)
    RehireDate = models.DateField(("Date"))
    Region = models.CharField(max_length = 100)
    BusinessUnit = models.CharField(max_length = 100)
    DeptID = models.CharField(max_length = 100)
    DepartmentName = models.CharField(max_length = 100)
    ServiceLine = models.CharField(max_length = 100)
    WorkLocationCode = models.CharField(max_length = 100)
    EmployeeName = models.CharField(max_length = 100)
    PositionNumber = models.CharField(max_length = 100)
    JobCode = models.CharField(max_length = 100)
    UnionCd = models.CharField(max_length = 100)
    RegTemp = models.CharField(max_length = 100)
    FTPTPD = models.CharField(max_length = 100)
    StdHrs = models.CharField(max_length = 100)
    FTE = models.CharField(max_length = 100)
    JobFunctionFamily = models.CharField(max_length = 100)
    MgrLvl = models.CharField(max_length = 100)
    HireDate = models.CharField(max_length = 100)
    ReportsToName = models.CharField(max_length = 100)
    ReportsToEmplid = models.CharField(max_length = 100)
    ReportsToPositionnumber = models.CharField(max_length = 100)
    WorkEmail = models.CharField(max_length = 100)
    Gender = models.CharField(max_length = 100)
    EthnicityRace = models.CharField(max_length = 100)
    ActionReason = models.CharField(max_length = 100)
    ActionReasonDesc = models.CharField(max_length = 100)
    
    
class Transfers(models.Model):
      Emplid = models.CharField(max_length = 100)
      EmployeeName = models.CharField(max_length = 100)
      EffectiveDate = models.DateField(("Date"))
      WorkEmail = models.CharField(max_length = 100)
      Gender = models.CharField(max_length = 100)
      EthnicityRace = models.CharField(max_length = 100)
      ActionReason = models.CharField(max_length = 100)
      ActionReasonDesc = models.CharField(max_length = 100)
      ReasonBucket = models.CharField(max_length = 100)
      
      Region_From = models.CharField(max_length = 100)
      BusinessUnit_From = models.CharField(max_length = 100)
      DeptID_From = models.CharField(max_length = 100)
      DepartmentName_From = models.CharField(max_length = 100)
      ServiceLine_From = models.CharField(max_length = 100)
      WorkLocationCode_From = models.CharField(max_length = 100)
      PositionNumber_From = models.CharField(max_length = 100)
      JobCode_From = models.CharField(max_length = 100)
      UnionCd_From = models.CharField(max_length = 100)
      RegTemp_From = models.CharField(max_length = 100)
      FTPTPD_From = models.CharField(max_length = 100)
      StdHrs_From = models.CharField(max_length = 100)
      FTE_From = models.CharField(max_length = 100)
      JobFunctionFamily_From = models.CharField(max_length = 100)
      MgrLvl_From = models.CharField(max_length = 100)
      
      Region_To = models.CharField(max_length = 100)
      BusinessUnit_To = models.CharField(max_length = 100)
      DeptID_To = models.CharField(max_length = 100)
      DepartmentName_To = models.CharField(max_length = 100)
      ServiceLine_To = models.CharField(max_length = 100)
      WorkLocationCode_To = models.CharField(max_length = 100)
      PositionNumber_To = models.CharField(max_length = 100)
      JobCode_To = models.CharField(max_length = 100)
      UnionCd_To = models.CharField(max_length = 100)
      RegTemp_To = models.CharField(max_length = 100)
      FTPTPD_To = models.CharField(max_length = 100)
      StdHrs_To = models.CharField(max_length = 100)
      FTE_To = models.CharField(max_length = 100)
      JobFunctionFamily_To = models.CharField(max_length = 100)
      MgrLvl_To = models.CharField(max_length = 100)



#Specialty Models
class HROps_Headcount(models.Model):
    ReportDate = models.DateField(("Date"))
    Category = models.CharField(max_length = 100)
    Region = models.CharField(max_length = 100)
    BU_SL = models.CharField(max_length = 100)
    Headcount_Demographic_Full = models.IntegerField()
    Headcount_Demographic_CYFiltered = models.IntegerField()
    Headcount_Demographic_PYFiltered = models.IntegerField()
    Headcount_Hires_TTM = models.IntegerField()
    Headcount_XFRs_TTM = models.IntegerField()
    Headcount_Terms_TTM = models.IntegerField()
    Headcount_XFR_Lateral_TTM = models.IntegerField()
    Headcount_XFR_Promotion_TTM = models.IntegerField()
    Headcount_XFR_Demotion_TTM = models.IntegerField()
    TurnoverPct_TTM = models.DecimalField(max_digits=10,decimal_places=3)
    

class JobCodeTable(models.Model):
    JobCode = models.CharField(max_length = 100, default="N/A")
    JobTitle = models.CharField(max_length = 1000, default="N/A")
    StdHrs = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    SalaryPlan = models.CharField(max_length = 10,default="N/A")
    Grade = models.CharField(max_length = 10,default="N/A")
    UnionCode = models.CharField(max_length = 10,default="N/A")
    FLSA = models.CharField(max_length = 10,default="N/A")
    JobFunction = models.CharField(max_length = 10,default="N/A")
    JobFamily = models.CharField(max_length = 10,default="N/A")
    JobGroup = models.CharField(max_length = 10,default="N/A")
    MgrLvl = models.CharField(max_length = 10,default="N/A")
    OccupCode = models.CharField(max_length = 10,default="N/A")
    WorkersComp = models.CharField(max_length = 10,default="N/A")
    PTOCode = models.CharField(max_length = 10,default="N/A")             
    
    
class SNA_Network(models.Model):
    #attributes based on sender
    ModelIndex = models.CharField(max_length = 100, default="N/A")
    Sender = models.CharField(max_length = 200)
    Recipient = models.CharField(max_length = 200)
    N = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    #attributes
    Department = models.CharField(max_length = 200, default="N/A")
    JobFunction = models.CharField(max_length = 10, default="N/A")
    Betweenness = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Closeness = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    
class AddressGeo(models.Model):
    LocCategory = models.CharField(max_length = 20,default="Home")
    LocationName = models.CharField(max_length = 2000,default="N/A")
    Address_Street = models.CharField(max_length = 2000,default="N/A")
    Address_City = models.CharField(max_length = 2000,default="N/A")
    Address_State = models.CharField(max_length = 10,default="N/A")
    Address_ZipCode = models.CharField(max_length = 20,default="N/A")
    Longitude = models.DecimalField(max_digits=12,decimal_places=8,default=0)
    Latitude = models.DecimalField(max_digits=12,decimal_places=8,default=0)
    EmpId = models.CharField(max_length = 20,default="N/A")
    