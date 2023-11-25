# Model Document: 序列化器; Viewset 1 queryset 2 serialize
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from utils.filters import MongoSearchFilter
from utils.permissions import CrudDocumentModelPermissions
from .models import CiType, Ci
from .serilallzers import CiTypeSerializer, CiSerializer, CiTypeWithFiledsSerializer
from rest_framework.decorators import action


class CiTypeViewSet(viewsets.ModelViewSet): # CRUD
    queryset = CiType.objects.all()
    serializer_class = CiTypeSerializer
    permission_classes = [IsAuthenticated, CrudDocumentModelPermissions]

    filter_backends = [MongoSearchFilter] # 控制搜索使用的搜索类
    search_fields = ['label']

    # CRUD基本操作已经完成
    # 1. action /cmdb/citypes/111/xxx/
    # 2. retrieve 覆盖 不好
    # 详情就应该带着fields 2好的
    # 个别情况下 详情需要fields 2不好
    # 不同况下 可以选择不如的序列化器
    def get_serializer_class(self):
        print(self.kwargs, '###################')
        if 'id' in self.kwargs:
            return CiTypeWithFiledsSerializer # 带着fields的序列化器
        return super().get_serializer_class()


    @action(detail=False)  # 不是详情页
    def all(self, request):
        # TODO 只显示该类型的最后一个本本号的数据
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # /cmdb/citypes/Network 不用pk也能进行详情页的查询啊
    @action(detail=False, url_path="(?P<name>[^/.]+)/(?P<version>\d+)") # 不是详情页 详情页后面必须是id
    def get_object_by_name_and_version(self, request, name, version):
        # obj = self.get_object() # 使用这个的时候必须使用pk
        obj = self.get_queryset().get(name=name, version=version)
        serializer = CiTypeWithFiledsSerializer(obj)
        return Response(serializer.data)

class CiViewSet(viewsets.ModelViewSet):
    queryset = Ci.objects()
    serializer_class = CiSerializer
    permission_classes = [IsAuthenticated, CrudDocumentModelPermissions]
    # CRUD基本操作提供Mixin提供

print(CiTypeViewSet.queryset.__dict__.keys(), "-----------------------------------------------------1") # 看属性中都有什么



