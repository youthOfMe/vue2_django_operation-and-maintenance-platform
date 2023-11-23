from django.urls import path
from .views import CiTypeViewSet, CiViewSet
from rest_framework_mongoengine import routers

router = routers.SimpleRouter()
router.register('citypes', CiTypeViewSet) # /cmdb/
router.register('cis', CiViewSet)

urlpatterns = [] + router.urls
print(urlpatterns)