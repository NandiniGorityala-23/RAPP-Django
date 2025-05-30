from rest_framework import serializers
from api.models import ProjectDetails,ClientDetails


class ProjectDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProjectDetails
		fields = ('project_code','client_code','projectname','pm_emp_id','SOW','project_start_date','project_end_date','BU_head','billing_type','ts')

class ClientDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = ClientDetails
		fields =('client_code','client_name','client_location','billing_entity','MSA','MSA_start_date','MSA_end_date')
