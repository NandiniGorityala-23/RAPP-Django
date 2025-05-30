from rest_framework import serializers
from api.models import JobDetails,Skillset,Employee


class JobSerializer(serializers.ModelSerializer):

	class Meta:
		model = JobDetails
		fields = ('rec_id','pm_emp_id','project_code','client_name','no_of_positions','experience',\
			'qualification','designation','job_type','client_interview','demand_type',\
			'request_type','skill_set','location','billable','status','job_description',\
			'bill_date','on_board_date','interview_details','approved_by','interview_remarks','ts')

class SkillSerializer(serializers.ModelSerializer):

	class Meta:
		model = Skillset
		fields = ('emp_id','skill_set','experience')

class EmployeeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Employee
		fields = ('emp_id','name','msysemail','location','is_active')
