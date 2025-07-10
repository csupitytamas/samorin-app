from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .permissions import IsAdminAndNotTargetAdmin
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminAndNotTargetAdmin]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminAndNotTargetAdmin]

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)