from rest_framework import serializers
from .models import Organization

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'