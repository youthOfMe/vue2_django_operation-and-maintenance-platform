from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import OrgSerializer, Organization
from rest_framework.decorators import action

class OrgViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    permission_classes = []

    @action(detail=False)
    def tree(self, request):
        queryset = self.get_queryset()

        nodes = {} # 所有节点对象都进来 key id, value data
        results = []
        for o in queryset:
            id = o.id
            pid = o.parent_id
            data = self.get_serializer(o).data
            data.setdefault('children', []) # 序列化器中的设置数据的方法
            nodes[id] = data # 考虑父级永远出现在子级的前边

            if pid:
                nodes[pid]['children'].append(data)
            else:
                results.append(data)

        # serializer = self.get_serializer(queryset, many=True) # 可以使用get_serializer拿到序列化器 serializer.data里面是数据

        return Response({ 'results': results })
