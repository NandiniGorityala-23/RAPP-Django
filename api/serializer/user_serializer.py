from rest_framework import serializers
from api.models import UserAdmin

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAdmin
		fields = ('user_name','emp_id')