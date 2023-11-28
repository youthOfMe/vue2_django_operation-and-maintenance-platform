from rest_framework import serializers
from .models import Organization, Host


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        extra_kwargs = {
            'password': { 'write_only': True },
            'ssh_pkey_path': { 'write_only': True }
        }
