from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, PoleViewSet, WingsViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'poles', PoleViewSet)
router.register(r'wings', WingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]