from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view

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

