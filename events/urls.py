from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ArenaViewSet, PoleLocationViewSet, WingLocationViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'arenas', ArenaViewSet)
router.register(r'pole-locations', PoleLocationViewSet)
router.register(r'wing-locations', WingLocationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]