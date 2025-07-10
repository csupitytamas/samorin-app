from rest_framework import viewsets
from .models import Wishlist
from .permissions import IsChiefOrAdmin
from .serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    permission_classes = [IsChiefOrAdmin] # vagy a saját IsChiefOrAdmin, ha csak ők használhatják
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)