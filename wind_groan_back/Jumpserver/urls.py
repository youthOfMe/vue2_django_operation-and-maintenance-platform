from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import OrgViewSet, HostViewSet, upload

router = SimpleRouter()
router.register('orgs', OrgViewSet)
router.register('hosts', HostViewSet)


urlpatterns = router.urls + [
    path('upload/', upload)
]