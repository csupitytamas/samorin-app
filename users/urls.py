from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserListView, UserProfileViewSet, UserMeView

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('', include(router.urls)),   # ← ezt tedd hozzá!
    path('me/', UserMeView.as_view(), name='user-me'),
]