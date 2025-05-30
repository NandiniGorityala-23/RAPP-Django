from rest_framework import serializers
from api.models import CandidateFeedback

class CandidateFeedbackSerializer(serializers.ModelSerializer):
	rec_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = CandidateFeedback
		# fields = "__all__"
		exclude = ('ts', )