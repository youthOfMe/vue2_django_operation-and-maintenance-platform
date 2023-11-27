from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import OrgSerializer, Organization

class OrgViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    permission_classes = []
