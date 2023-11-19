from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from User.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'password', 'is_superuser', 'username', 'is_active', 'phone', 'email'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'default': False},
            'is_active': {'default': False},
            'username': {'min_length': 3, 'max_length': 16},
        }

    def validate_password(self, value):
        # 使用正则进行分析 密码的强弱
        if 4 <= len(value) <= 16:
            return make_password(value)
        raise serializers.ValidationError('The length og password')

# 可以在这里进行校验密码
class PwdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        # 使用正则进行分析 密码的强弱
        if 4 <= len(value) <= 16:
            return make_password(value)
        raise serializers.ValidationError('The length og password')