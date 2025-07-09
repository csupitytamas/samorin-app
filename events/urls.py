from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ArenaViewSet, PoleLocationViewSet, WingLocationViewSet, ArchivedEventDetailView, \
    ArchivedEventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'arenas', ArenaViewSet)
router.register(r'pole-locations', PoleLocationViewSet)
router.register(r'wing-locations', WingLocationViewSet)
router.register(r'archived-events', ArchivedEventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('archived-events/<int:pk>/', ArchivedEventDetailView.as_view(), name='archived-event-detail'),
]