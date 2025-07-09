from rest_framework import viewsets
from .models import Warehouse, Pole, Wings
from .serializers import WarehouseSerializer, PoleSerializer, WingsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsAdminOrReadOnly

class WarehouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class PoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Pole.objects.all()
    serializer_class = PoleSerializer
    parser_classes = [MultiPartParser, FormParser]

class WingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Wings.objects.all()
    serializer_class = WingsSerializer
    parser_classes = [MultiPartParser, FormParser]