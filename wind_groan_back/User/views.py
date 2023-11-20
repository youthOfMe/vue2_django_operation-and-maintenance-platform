import django_filters.rest_framework
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http.response import HttpResponse, Http404
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from User.models import UserProfile
from User.serializers import UserSerializer, PwdSerializer, PermSerializer, GroupSerializer
from utils.exceptions import InvalidPassword
from django.contrib.auth.models import Permission, Group, ContentType

_exclude_content_types = [
    c.id for c in ContentType.objects.filter(model__in=[
        'logentry', 'group',    'permission',
        'contenttype', 'session'
    ])
]
# 写全局变量，只执行一次 可多次使用

# 权限接口
class PermViewSet(ModelViewSet):
    # 根据有pk就是根据主键 进行过滤相关数据 在接口里进行
    queryset = Permission.objects.exclude(content_type__in=_exclude_content_types).order_by('pk')
    serializer_class = PermSerializer
    search_fields = ['name', 'codename']

class RoleViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(['GET'], detail=True, url_path='perms')
    def perms(self, request, pk=None):
        obj = self.get_object()

        data = self.serializer_class(obj).data
        data['allPerms'] = list(PermViewSet.queryset.values('id', 'name')) # 查询集不能直接进行序列化 只能是字典/列表
        return Response(data)



class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['username'] # 严格等于 多个条件是and
    # filter_backends = [SearchFilter]
    search_fields = ['username', 'email'] # 指定在哪些字段进行模糊搜索

    # 重写获取角色信息的函数
    @action(['GET'], True, 'roles')
    def roles(self, request, pk=None):
        user = self.get_object()
        data = UserSerializer(user).data
        # roles = user.groups.all()
        data['roles'] = [ u.id for u in user.groups.all() ]
        data['allRoles'] = Group.objects.values('id', 'name') # 不能序列化集合 只能转换为字典

        return Response(data)

    # 进行给用户安排角色
    # @action(['PATCH'], True, 'setroles')
    @roles.mapping.put # 使用roles的patch方法时隐射到这个函数
    def setroles(self, request, pk=None): # 详情页是必须提供pk
        user = self.get_object()
        roles = request.data.get('roles', None)
        if roles is None:
            pass
        else:
            user.groups.set(roles)

        return Response(status=201)

    # 权限
    # permission_classers = [IsAdminUser] # 必须是管理员
    # 1. 覆盖分页list方法 只影响查询列表功能 但是这样要对查询完的结果再进行修改很麻烦
    # 在此进行重写list函数 可在收到查询结果前进行得到结果
    # def list(self, request, *args, **kwargs):
    #     queryset = super().get_queryset()
    #     username = request.query_params.get('username', None)
    #     if username:
    #         queryset = queryset.filter(username__icontains=username)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    # 2. 重写这个方法 对全局查询有影响
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # 对queryset进行处理
    #     return queryset

    # 如果想自定义增删改查就使用这个方法
    # 默认路由地址 users/w/
    # 查询登录的用户信息
    @action(detail=False, url_path='whoami') #  是否是详情 detail为True 参数至少要有pk
    def w(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

    # 进行修改密码
    @action(['PATCH'], detail=True, url_path='chpwd')
    def chpwd(self, request, pk=None):
        user = request.user
        old = request.data.get('oldPassword', '')
        # serializer = PwdSerializer()
        if user.check_password(old):
            user.set_password(request.data.get('password', ''))
            user.save()
        else:
            raise InvalidPassword

        return Response()

    # 进行编写重置密码

    # 重新更新函数 对patch和put都管用
    # def update(self, request, *args, **kwargs):
    #     pass

    # 重写更新函数 只对patch管用
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('password', None)
        request.data.pop('id', None)

        return super().partial_update(request, *args, **kwargs)

    # 防止超级管理员被删除
    # 1. 在update, destory方法中 进行id的判断 如果为1 抛异常
    # 2. 详情页三个方法都需要使用get_object pk
    def get_object(self):
        # pk
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == '1' or pk == 1:
                raise Http404

        return super().get_object()



# 必须登录了
# @login_required
def userlogin(request):
    # 能到视图函数, 就一定通过了前面的中间件的process_request
    print(1, request.user) #  从session标中通过sessionkey查session_data 认证中间件帮我们查了user_id 用user_id查auth_user表
    print(2, request.session)
    if request.user.is_authenticated:
        print(4, '我真的是User的实例')
    # if isinstance(request.user, User):
    #     print(4, '我真的是User的实例')
    user = authenticate(username='admin', password='123456')
    print(3, user)
    if user:
        login(request, user) # request.user token => sessionid, session_data, user_id
        # response阶段, 中借鉴还会生成set-cookie sessionid
    return HttpResponse('我成功login')

@api_view(['GET', 'POST'])
def test_jwt_login(request:Request):
    # 由于我们设置了DRF全局认证类 那么进入视图的时候应该是认证过了
    print('~' * 30)
    print(1, request.COOKIES, request._request.COOKIES, request._request.headers)
    print(2, request.data) # json drf --> dict
    print(3, request.user, request.user.is_authenticated)
    print(4, request.auth)
    print('~' * 30)
    return Response()

class MenuItem(dict):
    def __init__(self, id, name, path=None):
        super()
        self['id'] = id
        self['name'] = name
        self['path'] = path # 告诉前端静态路由
        self['children'] = []

    # 访问属性的时候就写会进行执行这个
    def __getattr__(self, item):
        return self[item]

    @property
    def children(self):
        return self['children']

    def append(self, subitem):
        self['children'].append(subitem)
        return self

    def __add__(self, other):
        self['children'].append(other)

@api_view() # GET
@permission_classes([IsAuthenticated])
# staff代表admin管理员
# @permission_classes([IsAuthenticated, IsAdminUser]) 第一个登录就可以 第二个必须is_staff = 1 是管理员才行
def menulist_view(request):
    print(request.user) # user
    print(request.auth) # token
    # 菜单数据哪里来
    # 1. 数据库李存着, 反复拿这个不怎么变化的菜单
    # 2. 写死
    menulist = []

    if request.user:
        itemA = MenuItem(0, '首页', '/welcome')
        itemB = MenuItem(2, 'CMDB资产管理', '/welcome')
        itemC = MenuItem(3, '堡垒机', '/welcome')
        item = MenuItem(1, '用户管理') # 管理员权限
        item.children.append(MenuItem(101, '用户列表', '/users'))
        item.children.append(MenuItem(102, '角色列表', '/users/roles'))
        item + MenuItem(103, '权限列表', '/users/perms')

        menulist.append(itemA)
        menulist.append(item)
        menulist.append(itemB)
        menulist.append(itemC)

    return Response(menulist)