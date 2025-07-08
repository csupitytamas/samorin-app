from rest_framework.routers import DefaultRouter
from .views import PoleViewSet, WingsViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'poles', PoleViewSet)
router.register(r'wings', WingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]