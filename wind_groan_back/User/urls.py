from django.urls import  path
from .views import test_jwt_login

urlpatterns = [
    path('test/', test_jwt_login)
]