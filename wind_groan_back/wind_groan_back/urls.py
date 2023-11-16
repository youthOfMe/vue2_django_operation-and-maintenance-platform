"""
URL configuration for wind_groan_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from User.views import userlogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # 没有提供CRUD 提供了与数据库的关系(queryset, serializer_class)
    TokenRefreshView, #
)

tobview = TokenObtainPairView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', tobview, name="login"), # /login/ 用户登录的路由
    path('token/', tobview, name='token_obtain_pair'), # 获取token 只支持post
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 刷新toekn
    # 测试
    path('user/', include('User.urls'))
]
