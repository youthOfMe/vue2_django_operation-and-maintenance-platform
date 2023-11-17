from django.urls import  path
from .views import test_jwt_login, menulist_view

urlpatterns = [
    path('test/', test_jwt_login),
    path('menulist/', menulist_view)
]