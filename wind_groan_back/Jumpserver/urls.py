from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import OrgViewSet

router = SimpleRouter()
router.register('orgs', OrgViewSet)

urlpatterns = router.urls