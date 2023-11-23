from rest_framework_mongoengine import serializers
from .models import CiType, Ci


# ODM 提供对Document序列化器
class CiTypeSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CiType
        # fields = '__all__'
        exclude = ['fields']

class CiTypeWithFiledsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CiType
        fields = '__all__'

class CiSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Ci
        fields = '__all__'