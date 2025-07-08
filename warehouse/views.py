from rest_framework import viewsets
from .models import Pole, Wings
from .serializers import PoleSerializer, WingsSerializer

class PoleViewSet(viewsets.ModelViewSet):
    queryset = Pole.objects.all()
    serializer_class = PoleSerializer

class WingsViewSet(viewsets.ModelViewSet):
    queryset = Wings.objects.all()
    serializer_class = WingsSerializer