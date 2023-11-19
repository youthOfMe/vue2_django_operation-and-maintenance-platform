from django.urls import  path
from .views import test_jwt_login, menulist_view, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('test/', test_jwt_login),
    path('menulist/', menulist_view)
] + router.urls

print('~' * 30)
print(urlpatterns)
print('~' * 30)