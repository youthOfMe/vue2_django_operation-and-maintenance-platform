from pathlib import Path

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Host
from .serializers import OrgSerializer, Organization, HostSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from datetime import datetime
import uuid

class OrgViewSet(ModelViewSet):
    queryset = Organization.objects.filter(is_deleted=False)
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

    def destroy(self, request, *args, **kwargs):
        # 实现逻辑删除

        print(kwargs, '---------------asdasdasd----')
        pk = kwargs.get('pk')

        target = []
        pids = [pk]
        if pk:
            # 这个方法是去找该接口类的sql语句中的查询该对象是否存在
            self.get_object() # 确定pk是否存在不存在就报错
            target.append(pk)
        while pids:
            if pids[0] is None:
                qs = self.get_queryset().filter(parent=None).values('id')
            else:
                qs = self.get_queryset().filter(parent__in=pids).values('id')
            cids = [ o['id'] for o in qs ]
            if cids:
                pids = cids
                target.extend(cids)
            else:
                break

        self.get_queryset().filter(pk__in=target).update(is_deleted=True) # queryset.update()

        return Response(status=204)

class HostViewSet(ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = []

# 给request注释一下类型
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload(request: Request):
    file_field_name = 'file'
    fileobj = request.data[file_field_name]
    # if fileobj.size > 1024:
    #     raise HugeFileSize('文件超过了配置的打小')
    basedir = Path(settings.JUMPSERVER_UPLOADS_BASE) # 基路径 使用path进行转通用路径
    # 相对路径 年/月/日 uid/年/月/日
    parentdir = Path('{}/{:%Y/%m/%d/%H}'.format(request.user.id, datetime.now())) # 进行格式化)
    filename = Path(uuid.uuid4().hex)
    # 目录在不在
    (basedir / parentdir).mkdir(parents=True, exist_ok=True)
    subdir = parentdir / filename
    # (basedir / parentdir / filename).write_bytes(fileobj.read()) # 小文件
    # 大文件按下面方式进行上传
    with open(basedir / subdir, 'wb') as f:
        for chunk in fileobj.chunks():
            f.write(chunk)

    return Response({ 'name': fileobj.name, 'url': str(subdir) })