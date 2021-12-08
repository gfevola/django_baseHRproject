from django import forms
from .models import Document, DataX, Demographic


class DocumentForm(forms.Form):
	#docfile = forms.FileField(
#			label='Select a file',
#			help_text = 'max. 43 megabytes'
#	)
	class Meta:
		model = Document
		fields = ('name','salary','location')
			
	
class DocText(forms.Form):
	class Meta:
		model = DataX
		fields = ('name','salary','location')
        
        

class DemoForm(forms.Form):
	reportname = forms.CharField(label='Report Date',max_length=12)
	class Meta:
		model = Demographic
		fields = ('Emplid', 'Region', 'BusinessUnit','DeptID', 'DepartmentName', 
                    'ServiceLine', 'WorkLocationCode', 'EmployeeName', 'PositionNumber', 'JobCode',
                    'UnionCd', 'RegTemp', 'FTPTPD', 'StdHrs', 'FTE', 'JobFunctionFamily', 'MgrLvl', # 'HireDate',
                    'ReportsToName', 'ReportsToEmplid', 'ReportsToPositionnumber', 
                    'WorkEmail', 'Gender', 'EthnicityRace')
